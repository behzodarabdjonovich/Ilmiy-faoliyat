from pathlib import Path
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.bot.states.letter import LetterForm
from app.bot.keyboards.common import types_kb,confirm_kb,result_kb
from app.database.repositories.users import get_or_create_user
from app.database.repositories.letters import create_letter,add_version,list_user_letters,get_owned_letter
from app.database.models import Letter, Organization
from app.services.ai_service import AIService
from app.services.document_service import create_docx
from app.services.pdf_service import create_pdf
router=Router(); ai=AIService()
@router.message(F.text=="📝 Yangi xat yaratish")
async def new(m:Message,state:FSMContext): await state.set_state(LetterForm.letter_type); await m.answer("Xat turini tanlang:",reply_markup=types_kb())
@router.message(LetterForm.letter_type)
async def s1(m:Message,state:FSMContext): await state.update_data(letter_type=m.text); await state.set_state(LetterForm.recipient); await m.answer("Qabul qiluvchi tashkilot:")
@router.message(LetterForm.recipient)
async def s2(m:Message,state:FSMContext): await state.update_data(recipient=m.text); await state.set_state(LetterForm.recipient_person); await m.answer("Qabul qiluvchi shaxs F.I.Sh. (yo‘q bo‘lsa -):")
@router.message(LetterForm.recipient_person)
async def s3(m:Message,state:FSMContext): await state.update_data(recipient_person=None if m.text=='-' else m.text); await state.set_state(LetterForm.recipient_position); await m.answer("Lavozimi (yo‘q bo‘lsa -):")
@router.message(LetterForm.recipient_position)
async def s4(m:Message,state:FSMContext): await state.update_data(recipient_position=None if m.text=='-' else m.text); await state.set_state(LetterForm.subject); await m.answer("Xat mavzusi:")
@router.message(LetterForm.subject)
async def s5(m:Message,state:FSMContext): await state.update_data(subject=m.text); await state.set_state(LetterForm.content); await m.answer("Asosiy mazmunni yozing:")
@router.message(LetterForm.content)
async def s6(m:Message,state:FSMContext): await state.update_data(content=m.text); await state.set_state(LetterForm.request); await m.answer("Aniq iltimos/talab/so‘rovni yozing:")
@router.message(LetterForm.request)
async def s7(m:Message,state:FSMContext): await state.update_data(request=m.text); await state.set_state(LetterForm.extra); await m.answer("Qo‘shimcha ma'lumot (yo‘q bo‘lsa -):")
@router.message(LetterForm.extra)
async def s8(m:Message,state:FSMContext): await state.update_data(extra=None if m.text=='-' else m.text); await state.set_state(LetterForm.signer); await m.answer("Imzolovchi F.I.Sh.:")
@router.message(LetterForm.signer)
async def s9(m:Message,state:FSMContext): await state.update_data(signer=m.text); await state.set_state(LetterForm.signer_position); await m.answer("Imzolovchi lavozimi:")
@router.message(LetterForm.signer_position)
async def s10(m:Message,state:FSMContext): await state.update_data(signer_position=m.text); await state.set_state(LetterForm.attachments); await m.answer("Ilovalar (yo‘q bo‘lsa -):")
@router.message(LetterForm.attachments)
async def s11(m:Message,state:FSMContext):
    await state.update_data(attachments=None if m.text=='-' else m.text); d=await state.get_data(); await state.set_state(LetterForm.confirm)
    await m.answer(f"Qabul qiluvchi: {d['recipient']}\nMavzu: {d['subject']}\nMazmun: {d['content']}",reply_markup=confirm_kb())
@router.callback_query(F.data=="letter:cancel")
async def cancel(c:CallbackQuery,state:FSMContext): await state.clear(); await c.message.answer("Bekor qilindi."); await c.answer()
@router.callback_query(F.data=="letter:generate")
async def generate(c:CallbackQuery,state:FSMContext,session:AsyncSession):
    d=await state.get_data(); u=c.from_user; dbu=await get_or_create_user(session,u.id,u.username,u.full_name)
    try: text=await ai.generate(d)
    except Exception: await c.message.answer("Xatni yaratishda vaqtinchalik xatolik yuz berdi. Iltimos, qayta urinib ko‘ring."); return
    letter=await create_letter(session,user_id=dbu.id,organization_id=None,letter_type=d['letter_type'],recipient=d['recipient'],recipient_person=d.get('recipient_person'),recipient_position=d.get('recipient_position'),subject=d['subject'],content=text,signer_name=d.get('signer'),signer_position=d.get('signer_position'),attachments=d.get('attachments'))
    await state.clear(); await c.message.answer(text,reply_markup=result_kb(letter.id)); await c.answer()
@router.callback_query(F.data.startswith("letter:revise:"))
async def revise_start(c:CallbackQuery,state:FSMContext,session:AsyncSession):
    lid=int(c.data.split(':')[-1]); letter=await get_owned_letter(session,lid,c.from_user.id)
    if not letter: await c.answer("Xat topilmadi yoki ruxsat yo‘q.",show_alert=True); return
    await state.update_data(letter_id=lid); await state.set_state(LetterForm.revise); await c.message.answer("Xatda nimani o‘zgartirishni xohlaysiz?"); await c.answer()
@router.message(LetterForm.revise)
async def revise_done(m:Message,state:FSMContext,session:AsyncSession):
    lid=(await state.get_data())['letter_id']; letter=await get_owned_letter(session,lid,m.from_user.id)
    if not letter: await m.answer("Xat topilmadi."); return
    text=await ai.revise(letter.content,m.text); await add_version(session,letter,text,m.text); await state.clear(); await m.answer(text,reply_markup=result_kb(letter.id))
@router.callback_query(F.data.startswith("letter:docx:"))
async def docx(c:CallbackQuery,session:AsyncSession):
    letter=await get_owned_letter(session,int(c.data.split(':')[-1]),c.from_user.id)
    if not letter: await c.answer('Xat topilmadi yoki ruxsat yo‘q.',show_alert=True); return
    org=await session.get(Organization,letter.organization_id) if letter.organization_id else None
    p=create_docx(letter,org,Path(f"storage/documents/letter_{letter.id}.docx")); await c.message.answer_document(FSInputFile(p)); await c.answer()
@router.callback_query(F.data.startswith("letter:pdf:"))
async def pdf(c:CallbackQuery,session:AsyncSession):
    letter=await get_owned_letter(session,int(c.data.split(':')[-1]),c.from_user.id)
    if not letter: await c.answer('Xat topilmadi yoki ruxsat yo‘q.',show_alert=True); return
    org=await session.get(Organization,letter.organization_id) if letter.organization_id else None
    p=create_pdf(letter,org,Path(f"storage/documents/letter_{letter.id}.pdf")); await c.message.answer_document(FSInputFile(p)); await c.answer()
@router.message(F.text=="📂 Mening xatlarim")
async def history(m:Message,session:AsyncSession):
    dbu=await get_or_create_user(session,m.from_user.id,m.from_user.username,m.from_user.full_name); items=await list_user_letters(session,dbu.id)
    if not items: await m.answer("Hozircha xatlar yo‘q."); return
    await m.answer("\n\n".join(f"📄 {x.letter_number or 'Draft'} — {x.subject} — {x.created_at:%d.%m.%Y}" for x in items))
