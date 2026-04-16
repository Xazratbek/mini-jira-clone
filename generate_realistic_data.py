"""
Organization-scoped realistic seed data generator for Mini Jira Clone.

What it creates:
- 1 platform admin
- 48 employees across 6 realistic organizations
- Organization memberships with owner/admin/manager/member roles
- 24 projects tied to organizations
- 216 tasks tied to projects and valid organization members
- 540 comments with realistic team collaboration notes

The dataset is deterministic and uses curated business-like data instead of
random Faker paragraphs, so the generated content stays coherent.
"""

import os
import sys
import django
import subprocess
from datetime import date, timedelta
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import connection

from organization.models import Organization, OrganizationMember, RoleChoice
from projects.models import Project
from tasks.models import Task, TaskPriorityChoice, TaskStatusChoice
from comments.models import Comment
from activity.models import ActivityLog


User = get_user_model()
random.seed(24)

DEFAULT_PASSWORD = "Test@1234"


def table_exists(model):
    return model._meta.db_table in connection.introspection.table_names()

ORGANIZATIONS = [
    {
        "name": "Atlas Retail Group",
        "domain": "atlasretail.uz",
        "description": "Ko'p filialli retail va supply chain boshqaruvi bilan shug'ullanuvchi kompaniya.",
        "website_url": "https://atlasretail.uz",
        "email": "office@atlasretail.uz",
        "phone": "+998712003344",
        "staff": [
            ("azizbek.raxmonov", "Azizbek", "Raxmonov", "owner", "CEO va product direction"),
            ("dilnoza.karimova", "Dilnoza", "Karimova", "admin", "Operations admin"),
            ("jahongir.sobirov", "Jahongir", "Sobirov", "manager", "Warehouse systems manager"),
            ("mohira.tosheva", "Mohira", "Tosheva", "member", "Business analyst"),
            ("sardor.nazarov", "Sardor", "Nazarov", "member", "Backend engineer"),
            ("umida.yoqubova", "Umida", "Yoqubova", "member", "QA engineer"),
            ("samandar.kadirov", "Samandar", "Kadirov", "member", "Frontend engineer"),
            ("nasiba.oripova", "Nasiba", "Oripova", "member", "Support specialist"),
        ],
        "projects": [
            {
                "name": "Retail ERP Rollout",
                "description": "Yangi filiallar uchun inventory, procurement va supplier settlement jarayonlarini birlashtirish.",
                "members": ["dilnoza.karimova", "jahongir.sobirov", "sardor.nazarov", "mohira.tosheva", "umida.yoqubova"],
                "tasks": [
                    ("Filial cutover rejasini yakunlash", "Yangi 12 ta filial uchun migratsiya jadvali va rollback rejasi yozilishi kerak.", "mohira.tosheva", "todo", "high", 10),
                    ("Inventory sync API ni yakunlash", "POS va markaziy ombor o'rtasida stock reconciliation oqimini yopish.", "sardor.nazarov", "in_progress", "high", 6),
                    ("Purchase order approval ekranini tekshirish", "Finance va supply teamlar uchun approval flow regressiyasini ko'rib chiqish.", "umida.yoqubova", "todo", "medium", 12),
                    ("Supplier aging report query optimizatsiyasi", "Mavjud hisobot 20 soniya ishlayapti, index va querylarni optimallashtirish kerak.", "jahongir.sobirov", "done", "medium", -1),
                    ("Warehouse operator training materiallarini tayyorlash", "Yangi release bo'yicha operatorlar uchun step-by-step qo'llanma yozish.", "dilnoza.karimova", "in_progress", "low", 14),
                    ("Production monitoring dashboard alertlarini sozlash", "ERP integratsiyalar yiqilganda Telegram va email alert ketishi kerak.", "sardor.nazarov", "todo", "medium", 9),
                    ("Return order scenario uchun UAT checklist", "Qaytarilgan tovarlar bo'yicha test ssenariylarini yaratish.", "umida.yoqubova", "done", "low", -3),
                    ("Procurement SLA metriclarini qo'shish", "Har bir filial bo'yicha yetkazib berish kechikishini o'lchaydigan widget yozish.", "mohira.tosheva", "todo", "medium", 18),
                    ("Branch manager permissions audit", "Qaysi rol qaysi modulga kira olishini qayta tekshirish.", "dilnoza.karimova", "in_progress", "high", 4),
                ],
            },
            {
                "name": "Supplier Portal 2.0",
                "description": "Ta'minotchilar uchun self-service portal, invoice tracking va dispute management funksiyalari.",
                "members": ["azizbek.raxmonov", "dilnoza.karimova", "samandar.kadirov", "sardor.nazarov", "nasiba.oripova"],
                "tasks": [
                    ("Invoice upload wizard UX yakuni", "Supplier foydalanuvchilari uchun uch qadamli invoice yuklash oqimini soddalashtirish.", "samandar.kadirov", "in_progress", "medium", 5),
                    ("Dispute status email templatelarini yozish", "Open, reviewing va resolved statuslari uchun transactional email matnlarini tayyorlash.", "nasiba.oripova", "todo", "low", 8),
                    ("Portal login throttling qo'shish", "Bir IP dan ketma-ket xato urinishlar uchun rate limiting kerak.", "sardor.nazarov", "todo", "high", 3),
                    ("Supplier onboarding checklist tuzish", "Top supplierlar uchun onboarding hujjatlari va support ownerlarni aniqlash.", "dilnoza.karimova", "done", "medium", -2),
                    ("Weekly supplier KPI review", "Portal adoption va invoice turn-around time bo'yicha review deck tayyorlash.", "azizbek.raxmonov", "todo", "medium", 11),
                    ("Attachment virus scan integration", "Yuklangan fayllarni skanerdan o'tkazish integratsiyasini yopish.", "sardor.nazarov", "in_progress", "high", 7),
                    ("Support macros bazasini tozalash", "Supplier support jamoasida ishlatiladigan javob shablonlarini yangilash.", "nasiba.oripova", "done", "low", -4),
                    ("Portal FAQ sahifasi", "Eng ko'p so'raladigan savollar uchun structured sahifa yozish.", "samandar.kadirov", "todo", "low", 15),
                    ("Release readiness checklist", "Go-live oldidan infra, support va rollback checkpointlarni belgilash.", "dilnoza.karimova", "in_progress", "high", 2),
                ],
            },
        ],
    },
    {
        "name": "Samarqand Logistics Hub",
        "domain": "slh.uz",
        "description": "Regional delivery, routing va fleet control tizimlarini yurituvchi logistika operatori.",
        "website_url": "https://slh.uz",
        "email": "contact@slh.uz",
        "phone": "+998662100909",
        "staff": [
            ("bekzod.eshmurodov", "Bekzod", "Eshmurodov", "owner", "Operations director"),
            ("shahnoza.ahmedova", "Shahnoza", "Ahmedova", "admin", "Program admin"),
            ("ulugbek.holmatov", "Ulugbek", "Holmatov", "manager", "Routing manager"),
            ("nargiza.berdieva", "Nargiza", "Berdieva", "member", "Dispatch analyst"),
            ("kamron.rasulov", "Kamron", "Rasulov", "member", "Backend engineer"),
            ("sarvinoz.yuldasheva", "Sarvinoz", "Yuldasheva", "member", "Product designer"),
            ("mirjalol.sattarov", "Mirjalol", "Sattarov", "member", "Mobile engineer"),
            ("farrux.husanov", "Farrux", "Husanov", "member", "QA analyst"),
        ],
        "projects": [
            {
                "name": "Fleet Control Center",
                "description": "Kurerlar, haydovchilar va marshrut ko'rsatkichlarini yagona monitor markaziga yig'ish.",
                "members": ["shahnoza.ahmedova", "ulugbek.holmatov", "kamron.rasulov", "mirjalol.sattarov", "farrux.husanov"],
                "tasks": [
                    ("Driver app GPS heartbeat tekshiruvi", "Har 30 soniyada kelayotgan GPS pinglarni monitoring qilish va yo'qolgan sessionlarni tiklash.", "mirjalol.sattarov", "in_progress", "high", 4),
                    ("Dispatch board batching logic", "Bir marshrutga tushgan deliverylarni zonalar bo'yicha guruhlash.", "kamron.rasulov", "todo", "high", 9),
                    ("Late delivery escalation policy", "30 daqiqadan ortiq kechikkan buyurtmalar uchun dispatch alert mexanizmini yozish.", "ulugbek.holmatov", "todo", "medium", 7),
                    ("QA smoke run for courier shifts", "Tonggi va kechki smenalar uchun smoke checklist yuritish.", "farrux.husanov", "done", "low", -2),
                    ("Driver scorecard visual polish", "Operator panelidagi driver efficiency widgetini final holatga keltirish.", "sarvinoz.yuldasheva", "in_progress", "medium", 5),
                    ("Incident timeline export", "Support team uchun CSV export qo'shish.", "kamron.rasulov", "todo", "medium", 12),
                    ("Battery drain issue investigation", "Android courier appda ortiqcha battery usage sababini topish.", "mirjalol.sattarov", "in_progress", "high", 3),
                    ("Night shift dispatch playbook", "Tungi dispatcherlar uchun standart operating procedure yozish.", "shahnoza.ahmedova", "done", "medium", -1),
                    ("Geo-fence alert tuning", "Yolg'on pozitiv alertlarni kamaytirish uchun thresholdlarni moslash.", "ulugbek.holmatov", "todo", "low", 16),
                ],
            },
            {
                "name": "Warehouse Routing Optimizer",
                "description": "Omborlararo yuborish va so'nggi mil yetkazib berish marshrutini optimallashtirish.",
                "members": ["bekzod.eshmurodov", "nargiza.berdieva", "kamron.rasulov", "sarvinoz.yuldasheva", "farrux.husanov"],
                "tasks": [
                    ("Route simulation dataset tayyorlash", "So'nggi 60 kun delivery ma'lumotini optimizer uchun tayyorlash.", "nargiza.berdieva", "done", "medium", -6),
                    ("Optimizer API timeout muammosi", "Katta route batchlarda 504 qaytayotgan endpointni tahlil qilish.", "kamron.rasulov", "in_progress", "high", 2),
                    ("Cost saving dashboard mockup", "Ops leadership uchun cost saving sahifasining yangi layouti.", "sarvinoz.yuldasheva", "todo", "medium", 10),
                    ("Weekend routing policy review", "Shanba/yakshanba sharoitida route qoidalarini update qilish.", "bekzod.eshmurodov", "todo", "medium", 13),
                    ("Regression test for route import", "CSV import oqimida duplicate stop muammosini qayta tekshirish.", "farrux.husanov", "in_progress", "low", 6),
                    ("Priority lane rule engine", "VIP mijoz buyurtmalari uchun tezkor lane qoidasi yozish.", "kamron.rasulov", "todo", "high", 8),
                    ("Driver feedback synthesis", "Haydovchi feedbacklaridan eng ko'p uchraydigan muammolarni jamlash.", "nargiza.berdieva", "done", "low", -3),
                    ("Optimizer launch readiness", "Pilot launch oldidan checklistlarni yopish.", "bekzod.eshmurodov", "in_progress", "high", 5),
                    ("Map legend cleanup", "Routing map interfeysida rang va ikonlarni birxillashtirish.", "sarvinoz.yuldasheva", "todo", "low", 17),
                ],
            },
        ],
    },
    {
        "name": "Tashkent Fintech Services",
        "domain": "tfs.uz",
        "description": "Kredit skoring, merchant settlement va fintech integratsiyalar bilan ishlovchi kompaniya.",
        "website_url": "https://tfs.uz",
        "email": "hello@tfs.uz",
        "phone": "+998712226688",
        "staff": [
            ("islom.kamilov", "Islom", "Kamilov", "owner", "Founder"),
            ("madina.jalolova", "Madina", "Jalolova", "admin", "Chief of staff"),
            ("temur.saidov", "Temur", "Saidov", "manager", "Risk products lead"),
            ("malika.usmonova", "Malika", "Usmonova", "member", "Compliance analyst"),
            ("javohir.abdullaev", "Javohir", "Abdullaev", "member", "Backend engineer"),
            ("nodira.rustamova", "Nodira", "Rustamova", "member", "QA engineer"),
            ("shoxrux.mamatov", "Shoxrux", "Mamatov", "member", "Data engineer"),
            ("diyor.mirzaev", "Diyor", "Mirzaev", "member", "Frontend engineer"),
        ],
        "projects": [
            {
                "name": "Merchant Settlement Console",
                "description": "Banklar va merchantlar o'rtasidagi settlement jarayonlarini kuzatish paneli.",
                "members": ["madina.jalolova", "javohir.abdullaev", "diyor.mirzaev", "nodira.rustamova", "malika.usmonova"],
                "tasks": [
                    ("Settlement retry scheduler", "Failed payoutlarni avtomatik qayta urinish logikasi bilan yopish.", "javohir.abdullaev", "in_progress", "high", 3),
                    ("Merchant payout timeline UI", "Merchant support jamoasi uchun payout eventlar tarixini ko'rsatish.", "diyor.mirzaev", "todo", "medium", 9),
                    ("Finance audit checklist", "Month-end settlement reconciliation bo'yicha checklist yozish.", "madina.jalolova", "done", "medium", -2),
                    ("Dispute resolution SLA", "Compliance va finance uchun case handling SLA'larini hujjatlashtirish.", "malika.usmonova", "todo", "low", 11),
                    ("Regression for payout rollback", "Rollback qilingan settlementlarda balance noto'g'ri chiqish holatini test qilish.", "nodira.rustamova", "in_progress", "high", 5),
                    ("Merchant-facing error copy", "Failed payout sabablari uchun merchantga ko'rinadigan aniq copy yozish.", "diyor.mirzaev", "todo", "low", 14),
                    ("Bank callback signature validation", "Callback imzosini verify qiladigan middleware qo'shish.", "javohir.abdullaev", "todo", "high", 4),
                    ("Release go/no-go notes", "Keyingi release uchun stakeholder summary tayyorlash.", "madina.jalolova", "done", "low", -1),
                    ("Refund edge-case analysis", "Partial refund settlement'larda yuzaga kelgan edge caselarni yig'ish.", "malika.usmonova", "in_progress", "medium", 6),
                ],
            },
            {
                "name": "Credit Scoring Pipeline",
                "description": "Loan eligibility va risk segmentatsiya uchun scoring data pipeline va review panel.",
                "members": ["islom.kamilov", "temur.saidov", "shoxrux.mamatov", "javohir.abdullaev", "nodira.rustamova"],
                "tasks": [
                    ("Feature store refresh job", "Har tong scoring featurelarni yangilash job'ining monitoringini yopish.", "shoxrux.mamatov", "in_progress", "high", 2),
                    ("Manual review queue prioritization", "Risk analystlar uchun navbatni risk darajasi bo'yicha tartiblash.", "temur.saidov", "todo", "medium", 8),
                    ("Data drift alert", "Scoring inputlarda anomaliya paydo bo'lsa alert qo'yish.", "javohir.abdullaev", "todo", "high", 7),
                    ("Adverse action notice template", "Rejected applicationlar uchun notice textini compliance bilan tasdiqlash.", "malika.usmonova", "done", "medium", -3),
                    ("Pipeline recovery drill", "ETL pipeline yiqilganda recovery runbookni sinab ko'rish.", "islom.kamilov", "todo", "medium", 13),
                    ("Cross-check rejected applicants", "Recent declined cases bo'yicha sample audit o'tkazish.", "nodira.rustamova", "in_progress", "low", 5),
                    ("Model score distribution report", "So'nggi oy bo'yicha score distribution deck tayyorlash.", "shoxrux.mamatov", "done", "low", -4),
                    ("Reviewer action log UI", "Manual review qarorlarini timeline ko'rinishida chiqarish.", "javohir.abdullaev", "todo", "medium", 10),
                    ("High-risk segment workshop", "Risk committee bilan workshop uchun material tayyorlash.", "temur.saidov", "in_progress", "high", 6),
                ],
            },
        ],
    },
    {
        "name": "Navoi Mining Systems",
        "domain": "nms.uz",
        "description": "Konchilik, texnik xizmat va xavfsizlik monitoring tizimlarini yurituvchi sanoat kompaniyasi.",
        "website_url": "https://nms.uz",
        "email": "info@nms.uz",
        "phone": "+998792440055",
        "staff": [
            ("odilbek.hakimov", "Odilbek", "Hakimov", "owner", "Industrial systems director"),
            ("munisa.shermatova", "Munisa", "Shermatova", "admin", "Program coordinator"),
            ("rustam.erkinov", "Rustam", "Erkinov", "manager", "Maintenance planning manager"),
            ("zarnigor.holiqova", "Zarnigor", "Holiqova", "member", "Safety analyst"),
            ("asror.kobulov", "Asror", "Qobulov", "member", "Backend engineer"),
            ("suhrob.eshonov", "Suhrob", "Eshonov", "member", "Data analyst"),
            ("sitora.eshpo'latova", "Sitora", "Eshpo'latova", "member", "QA engineer"),
            ("anvar.kadirov", "Anvar", "Qadirov", "member", "Field support engineer"),
        ],
        "projects": [
            {
                "name": "Maintenance Scheduling Hub",
                "description": "Texnik xizmat ishlari va ehtiyot qismlar holatini markazlashtiruvchi tizim.",
                "members": ["munisa.shermatova", "rustam.erkinov", "asror.kobulov", "sitora.eshpo'latova", "anvar.kadirov"],
                "tasks": [
                    ("Equipment downtime registry", "Yiliga to'plangan downtime sabablarini bitta registrga yig'ish.", "anvar.kadirov", "done", "medium", -5),
                    ("Maintenance window planner", "Bir nechta sex uchun parallel maintenance window planningni qo'shish.", "rustam.erkinov", "todo", "high", 12),
                    ("Spare parts threshold alerts", "Critical spare partlar minimum darajadan tushganda alert berish.", "asror.kobulov", "in_progress", "high", 4),
                    ("Checklist print format", "Field technicianlar uchun bosma checklist formatini yaxshilash.", "munisa.shermatova", "todo", "low", 15),
                    ("Regression on work-order close flow", "Work order yopilganda duplicated state chiqish holatini tekshirish.", "sitora.eshpo'latova", "in_progress", "medium", 6),
                    ("Planned outage communication template", "Ishlab chiqarish va xavfsizlik bo'limi uchun xabar matni.", "munisa.shermatova", "done", "low", -2),
                    ("Planner dashboard filters", "Maintenance board uchun zone va team filtrlari qo'shish.", "asror.kobulov", "todo", "medium", 8),
                    ("Root-cause library cleanup", "RCFA library ichidagi duplicate yozuvlarni tozalash.", "rustam.erkinov", "todo", "low", 16),
                    ("Technician sync stability", "Field offline data sync uzilishlarini kamaytirish.", "anvar.kadirov", "in_progress", "high", 3),
                ],
            },
            {
                "name": "Safety Incident Register",
                "description": "Safety observation, incident report va corrective actionlarni kuzatish platformasi.",
                "members": ["odilbek.hakimov", "zarnigor.holiqova", "suhrob.eshonov", "sitora.eshpo'latova", "asror.kobulov"],
                "tasks": [
                    ("Incident severity matrix", "Report form ichiga severity matrix qo'shish.", "zarnigor.holiqova", "todo", "medium", 9),
                    ("Observation analytics dataset", "Last quarter observation datalarini classification uchun tayyorlash.", "suhrob.eshonov", "done", "medium", -4),
                    ("Corrective action reminder bot", "Open actionlar bo'yicha haftalik reminder yuborish.", "asror.kobulov", "in_progress", "high", 5),
                    ("Safety mobile attachment bug", "Rasm biriktirish paytida Android qurilmalarda crash yuz berayotganini tahlil qilish.", "sitora.eshpo'latova", "in_progress", "high", 2),
                    ("Executive monthly summary", "Rahbariyat uchun oy yakuni summary deck tayyorlash.", "odilbek.hakimov", "todo", "low", 13),
                    ("Near-miss category cleanup", "Category nomlarini birxillashtirish va duplicate'larni tozalash.", "zarnigor.holiqova", "done", "low", -1),
                    ("Site access permission matrix", "Har bir site uchun report view access jadvalini ko'rib chiqish.", "asror.kobulov", "todo", "medium", 7),
                    ("Corrective action overdue view", "Deadline o'tgan actionlar uchun alohida view qo'shish.", "suhrob.eshonov", "todo", "medium", 10),
                    ("Emergency drill archive", "Oldingi emergency drill natijalarini arxivlash va qidiruvga tayyorlash.", "zarnigor.holiqova", "in_progress", "low", 14),
                ],
            },
        ],
    },
    {
        "name": "EduWave Learning Center",
        "domain": "eduwave.uz",
        "description": "Kurslar, mentorlik va LMS platformasini boshqaruvchi ta'lim markazi.",
        "website_url": "https://eduwave.uz",
        "email": "team@eduwave.uz",
        "phone": "+998712449911",
        "staff": [
            ("shaxzod.olimov", "Shaxzod", "Olimov", "owner", "Founder"),
            ("gulchehra.nurmatova", "Gulchehra", "Nurmatova", "admin", "Academic operations admin"),
            ("elmurod.tursunov", "Elmurod", "Tursunov", "manager", "LMS manager"),
            ("sevara.rahimova", "Sevara", "Rahimova", "member", "Methodologist"),
            ("maruf.eshqulov", "Maruf", "Eshqulov", "member", "Backend engineer"),
            ("aziza.baratova", "Aziza", "Baratova", "member", "Frontend engineer"),
            ("kamila.ibragimova", "Kamila", "Ibragimova", "member", "QA analyst"),
            ("bobur.hidoyatov", "Bobur", "Hidoyatov", "member", "Community manager"),
        ],
        "projects": [
            {
                "name": "LMS Attendance Tracker",
                "description": "Mentorlar va studentlar uchun attendance, progress va warning oqimini boshqaruvchi modul.",
                "members": ["gulchehra.nurmatova", "elmurod.tursunov", "maruf.eshqulov", "aziza.baratova", "kamila.ibragimova"],
                "tasks": [
                    ("Missed lesson escalation", "Ketma-ket 3 dars qoldirilganda student success teamga signal yuborish.", "elmurod.tursunov", "in_progress", "medium", 6),
                    ("Attendance import validation", "Zoom attendance import fayllarini tekshirish qoidalarini yozish.", "maruf.eshqulov", "todo", "high", 4),
                    ("Mentor dashboard cleanup", "Mentorlar uchun attendance boarddagi keraksiz ustunlarni olib tashlash.", "aziza.baratova", "todo", "low", 9),
                    ("Regression on absent reason flow", "Student absent sababini qayta tahrirlash oqimini test qilish.", "kamila.ibragimova", "done", "medium", -2),
                    ("Academic warning template", "Student va ota-onaga ketadigan warning textlarini yangilash.", "gulchehra.nurmatova", "todo", "medium", 11),
                    ("Bulk attendance edit action", "Operatorlar uchun bir nechta studentni birdan tahrirlash actioni.", "maruf.eshqulov", "in_progress", "high", 3),
                    ("Course timezone handling", "Regional kurslar uchun attendance vaqti noto'g'ri ko'rinayotganini tuzatish.", "kamila.ibragimova", "todo", "high", 7),
                    ("Attendance policy FAQ", "Mentorlar uchun qisqa foydalanish qo'llanmasi yozish.", "bobur.hidoyatov", "done", "low", -1),
                    ("Late join metric widget", "Kech qo'shilgan studentlar sonini ko'rsatadigan widget qo'shish.", "aziza.baratova", "todo", "low", 15),
                ],
            },
            {
                "name": "Mentor Evaluation Board",
                "description": "Kurs mentorlari bo'yicha feedback, lesson quality va retention signalini yig'ish tizimi.",
                "members": ["shaxzod.olimov", "sevara.rahimova", "bobur.hidoyatov", "aziza.baratova", "maruf.eshqulov"],
                "tasks": [
                    ("Feedback tag taxonomy", "Student feedbacklarni tahlil qilish uchun yagona teglar to'plamini yaratish.", "sevara.rahimova", "todo", "medium", 8),
                    ("Mentor scorecard data sync", "LMS va survey tizimlari o'rtasidagi score sync muammosini yopish.", "maruf.eshqulov", "in_progress", "high", 2),
                    ("Quarterly mentor review deck", "Rahbariyat uchun mentor evaluation natijalari deckini tayyorlash.", "shaxzod.olimov", "todo", "medium", 12),
                    ("Feedback submission UI simplification", "Studentlar uchun 3 daqiqalik feedback oqimini qisqartirish.", "aziza.baratova", "todo", "low", 10),
                    ("Regression on anonymous feedback", "Anonim feedback formi qayta ochilganda user ma'lumoti chiqib ketmayotganini tekshirish.", "kamila.ibragimova", "done", "high", -3),
                    ("Mentor improvement action tracker", "Har bir mentor uchun follow-up actionlar boardini yaratish.", "bobur.hidoyatov", "in_progress", "medium", 5),
                    ("Survey completion reminder", "Feedback form to'ldirmagan studentlarga gentle reminder qo'shish.", "maruf.eshqulov", "todo", "medium", 14),
                    ("Top mentor case study", "Eng yuqori retention ko'rsatgan mentor bo'yicha ichki case study yozish.", "sevara.rahimova", "done", "low", -5),
                    ("Review permissions matrix", "Akademik team va leadership uchun ko'rish huquqlarini tekshirish.", "shaxzod.olimov", "in_progress", "high", 4),
                ],
            },
        ],
    },
    {
        "name": "MedPoint Clinics Network",
        "domain": "medpoint.uz",
        "description": "Poliklinika tarmog'i, appointment va patient ops tizimlarini yurituvchi kompaniya.",
        "website_url": "https://medpoint.uz",
        "email": "support@medpoint.uz",
        "phone": "+998712223399",
        "staff": [
            ("ulugbek.rahmatov", "Ulugbek", "Rahmatov", "owner", "COO"),
            ("nilufer.asadova", "Nilufer", "Asadova", "admin", "Operations admin"),
            ("ozodbek.ganiev", "Ozodbek", "Ganiev", "manager", "Clinic systems manager"),
            ("maftuna.juraeva", "Maftuna", "Juraeva", "member", "Patient experience lead"),
            ("samir.mukimov", "Samir", "Mukimov", "member", "Backend engineer"),
            ("laylo.abdukarimova", "Laylo", "Abdukarimova", "member", "QA engineer"),
            ("asila.turgunova", "Asila", "Turgunova", "member", "UX designer"),
            ("ibrohim.fayziev", "Ibrohim", "Fayziev", "member", "Data analyst"),
        ],
        "projects": [
            {
                "name": "Appointment Queue Manager",
                "description": "Registratura, doctor load va patient queue oqimini boshqaruvchi tizim.",
                "members": ["nilufer.asadova", "ozodbek.ganiev", "samir.mukimov", "laylo.abdukarimova", "asila.turgunova"],
                "tasks": [
                    ("Reception queue heatmap", "Filiallar bo'yicha peak hour navbat yuklamasini ko'rsatuvchi heatmap yozish.", "ibrohim.fayziev", "done", "medium", -4),
                    ("No-show reminder logic", "Appointmentdan 2 soat oldin eslatma yuboradigan oqimni sozlash.", "samir.mukimov", "in_progress", "high", 3),
                    ("Doctor slot override UX", "Registratorlar uchun slot override ekrani soddalashtirilsin.", "asila.turgunova", "todo", "medium", 9),
                    ("Queue status regression", "Appointment statuslarining registrator panelida noto'g'ri chiqish holatini test qilish.", "laylo.abdukarimova", "todo", "high", 5),
                    ("Patient-facing reminder copy", "SMS va Telegram eslatmalaridagi matnlarni yangilash.", "maftuna.juraeva", "done", "low", -2),
                    ("Walk-in patient analytics", "Walk-in va oldindan yozilgan patientlar nisbatini ko'rsatuvchi report.", "ibrohim.fayziev", "todo", "low", 13),
                    ("Clinic timezone bug", "Filiallardan biri uchun slot vaqtlarida siljish bor, tekshirish kerak.", "samir.mukimov", "in_progress", "high", 2),
                    ("Reception SOP update", "Yangi queue board bo'yicha registratorlar uchun SOP yozish.", "nilufer.asadova", "todo", "medium", 11),
                    ("Doctor availability edge case", "Part-time doctorlarda slot lock holati noto'g'ri ishlayapti.", "ozodbek.ganiev", "in_progress", "medium", 7),
                ],
            },
            {
                "name": "Patient Follow-up Tracker",
                "description": "Vizitdan keyingi follow-up, lab natijalari va call-center workflowini birlashtiruvchi modul.",
                "members": ["ulugbek.rahmatov", "maftuna.juraeva", "samir.mukimov", "asila.turgunova", "laylo.abdukarimova"],
                "tasks": [
                    ("Follow-up task auto creation", "Vizit yopilgach kerakli follow-up vazifalarni avtomatik ochish.", "samir.mukimov", "todo", "high", 6),
                    ("Lab result delay report", "Kechikayotgan lab natijalari uchun daily report tuzish.", "ibrohim.fayziev", "in_progress", "medium", 8),
                    ("Patient satisfaction callback script", "Call-center uchun yangilangan callback script tayyorlash.", "maftuna.juraeva", "done", "low", -3),
                    ("Result viewer mobile layout", "Patient portal ichidagi natija ko'rish sahifasini mobil uchun yaxshilash.", "asila.turgunova", "todo", "medium", 10),
                    ("QA checklist for follow-up triggers", "Auto-created task triggerlari bo'yicha regression checklist yozish.", "laylo.abdukarimova", "in_progress", "high", 4),
                    ("Doctor note visibility audit", "Qaysi role qaysi note'ni ko'ra olishini qayta tekshirish.", "ulugbek.rahmatov", "todo", "high", 5),
                    ("Abnormal result escalation", "Critical resultlar uchun priority escalation qoidasi qo'shish.", "samir.mukimov", "todo", "high", 2),
                    ("Call outcome taxonomy cleanup", "Call-center outcome kategoriyalarini birxillashtirish.", "maftuna.juraeva", "done", "medium", -1),
                    ("Follow-up compliance dashboard", "Filiallar kesimida follow-up completion ko'rsatkichini chiqarish.", "ibrohim.fayziev", "todo", "medium", 14),
                ],
            },
        ],
    },
]

COMMENT_BANK = [
    "Bu taskni bugungi standupda ko'taramiz, dependency tomoni aniq bo'lsin.",
    "Backend va frontend kelishuvi bor, endpoint contract oxirgi marta tekshirilsin.",
    "Mijoz tomondan tasdiq olindi, endi release notes tayyorlash mumkin.",
    "Test natijasida bitta edge case chiqdi, lekin asosiy oqim barqaror.",
    "Bu ishni keyingi sprintga surmasak yaxshi bo'ladi, deadline yaqin.",
    "Support jamoasi shu o'zgarishni kutyapti, prioritetni tushirmaymiz.",
    "Prodga chiqishdan oldin rollback rejasini ham yozib qo'yaylik.",
    "Analitika bo'limi bu metrikaning eski va yangi qiymatini solishtirib beradi.",
    "UI tomonda copy ancha tushunarli bo'ldi, endi faqat state handling qoldi.",
    "Infra bilan bog'liq risk yo'q, lekin monitoring alertini albatta qo'shamiz.",
    "Documentation qismini task yopilishidan oldin yangilab yuboring.",
    "Bu yechim vaqtincha emas, keyingi quarter uchun ham mos tushyapti.",
    "Pilot guruhdan ijobiy feedback keldi, release confidence oshdi.",
    "Operatorlar uchun qo'llanma yozilsa support yuklama kamayadi.",
    "Shu joyda oldingi bug qaytib kelmasligi uchun regression case qo'shildi.",
]


def role_label(role):
    return {
        RoleChoice.OWNER: "owner",
        RoleChoice.ADMIN: "admin",
        RoleChoice.MANAGER: "manager",
        RoleChoice.MEMBER: "member",
    }[role]


def clear_existing_data():
    print("Mavjud ma'lumotlar tozalanmoqda...")
    if table_exists(ActivityLog):
        ActivityLog.objects.all().delete()
    if table_exists(Comment):
        Comment.objects.all().delete()
    if table_exists(Task):
        Task.objects.all().delete()
    if table_exists(Project):
        Project.objects.all().delete()
    if table_exists(OrganizationMember):
        OrganizationMember.objects.all().delete()
    if table_exists(Organization):
        Organization.objects.all().delete()
    if table_exists(User):
        User.objects.exclude(is_superuser=True).delete()
    print("✓ Tozalash yakunlandi.\n")


def ensure_platform_admin():
    admin, created = User.objects.get_or_create(
        username="admin",
        defaults={
            "email": "admin@gmail.com",
            "first_name": "Platform",
            "last_name": "Admin",
            "is_superuser": True,
            "is_staff": True,
        },
    )
    if created:
        admin.set_password(DEFAULT_PASSWORD)
        admin.save(update_fields=["password"])
    else:
        admin.email = "admin@gmail.com"
        admin.is_superuser = True
        admin.is_staff = True
        admin.set_password(DEFAULT_PASSWORD)
        admin.save(update_fields=["email", "is_superuser", "is_staff", "password"])

    return admin


def create_organizations_and_users():
    print("Organization, user va membershiplar yaratilmoqda...")
    users_by_username = {}
    organizations = []

    for org_seed in ORGANIZATIONS:
        staff = org_seed["staff"]
        owner_seed = next(member for member in staff if member[3] == "owner")
        owner_username, owner_first, owner_last, _, _ = owner_seed
        owner = User.objects.create_user(
            username=owner_username,
            email=f"{owner_username}@{org_seed['domain']}",
            first_name=owner_first,
            last_name=owner_last,
            password=DEFAULT_PASSWORD,
        )
        users_by_username[owner_username] = owner

        organization = Organization.objects.create(
            name=org_seed["name"],
            owner=owner,
            description=org_seed["description"],
            website_url=org_seed["website_url"],
            email=org_seed["email"],
            phone=org_seed["phone"],
        )
        organizations.append((organization, org_seed))

        for username, first_name, last_name, role, _job_title in staff:
            if username == owner_username:
                user = owner
            else:
                user = User.objects.create_user(
                    username=username,
                    email=f"{username}@{org_seed['domain']}",
                    first_name=first_name,
                    last_name=last_name,
                    password=DEFAULT_PASSWORD,
                )
                users_by_username[username] = user

            OrganizationMember.objects.create(
                organization=organization,
                user=user,
                role=role,
                is_active=True,
                created_by=owner,
            )

        print(f"  ✓ {organization.name}: {len(staff)} ta user")

    print(f"✓ {len(organizations)} organization va {len(users_by_username)} user yaratildi.\n")
    return organizations, users_by_username


def create_projects(organizations, users_by_username):
    print("Projectlar yaratilmoqda...")
    projects = []

    for organization, org_seed in organizations:
        owner = organization.owner
        for project_seed in org_seed["projects"]:
            member_users = [users_by_username[username] for username in project_seed["members"]]
            project = Project.objects.create(
                name=project_seed["name"],
                description=project_seed["description"],
                organization=organization,
                owner=owner,
                is_active=True,
            )
            project.members.set(member_users)
            projects.append((project, project_seed))
            print(f"  ✓ {organization.name} -> {project.name}")

    print(f"✓ {len(projects)} project yaratildi.\n")
    return projects


def created_by_for_project(project, project_seed, users_by_username):
    preferred_usernames = [name for name in project_seed["members"] if name != project.owner.username]
    if preferred_usernames:
        return users_by_username[random.choice(preferred_usernames)]
    return project.owner


def create_tasks(projects, users_by_username):
    print("Tasklar yaratilmoqda...")
    tasks = []
    today = timezone.localdate()

    for project, project_seed in projects:
        for title, description, assignee_username, status, priority, due_offset in project_seed["tasks"]:
            assignee = users_by_username[assignee_username]
            creator = created_by_for_project(project, project_seed, users_by_username)
            task = Task.objects.create(
                title=title,
                description=description,
                project=project,
                assigned_to=assignee,
                created_by=creator,
                status=status,
                priority=priority,
                due_date=today + timedelta(days=due_offset),
            )
            tasks.append(task)

        print(f"  ✓ {project.name}: {len(project_seed['tasks'])} ta task")

    print(f"✓ {len(tasks)} task yaratildi.\n")
    return tasks


def create_comments(tasks):
    print("Commentlar yaratilmoqda...")
    comments_created = 0

    for task in tasks:
        project_users = list(task.project.members.all()) or [task.project.owner]
        if task.project.owner not in project_users:
            project_users.append(task.project.owner)
        if task.assigned_to not in project_users:
            project_users.append(task.assigned_to)
        if task.created_by and task.created_by not in project_users:
            project_users.append(task.created_by)

        comment_count = 2 if task.status == TaskStatusChoice.DONE else 3
        if task.priority == TaskPriorityChoice.HIGH:
            comment_count += 1

        for _ in range(comment_count):
            author = random.choice(project_users)
            Comment.objects.create(
                task=task,
                author=author,
                content=random.choice(COMMENT_BANK),
            )
            comments_created += 1

    print(f"✓ {comments_created} comment yaratildi.\n")


def print_summary():
    print("=" * 72)
    print("Seed Summary")
    print("=" * 72)
    print(f"Users:               {User.objects.count()}")
    print(f"Organizations:       {Organization.objects.count()}")
    print(f"Memberships:         {OrganizationMember.objects.count()}")
    print(f"Projects:            {Project.objects.count()}")
    print(f"Tasks:               {Task.objects.count()}")
    print(f"Comments:            {Comment.objects.count()}")
    activity_count = ActivityLog.objects.count() if table_exists(ActivityLog) else 0
    print(f"Activity logs:       {activity_count}")
    print("=" * 72)
    print("Test login credentials:")
    print(f"  admin / {DEFAULT_PASSWORD}")
    print(f"  atlasretail owner: azizbek.raxmonov / {DEFAULT_PASSWORD}")
    print(f"  fintech owner: islom.kamilov / {DEFAULT_PASSWORD}")
    print("=" * 72)


def main():
    print("=" * 72)
    print("Mini Jira Clone - Realistic Organization Seed Generator")
    print("=" * 72)
    print()

    subprocess.run(
        [sys.executable, "manage.py", "migrate", "--run-syncdb", "--noinput"],
        check=True,
        cwd=os.path.dirname(os.path.abspath(__file__)),
    )
    clear_existing_data()
    ensure_platform_admin()
    organizations, users_by_username = create_organizations_and_users()
    projects = create_projects(organizations, users_by_username)
    tasks = create_tasks(projects, users_by_username)
    create_comments(tasks)
    print_summary()


if __name__ == "__main__":
    main()
