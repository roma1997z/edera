from django.shortcuts import render
from django.core.mail import send_mail

from landpage.models import MyOption, TeachersTZ, University, Contact, ContactForm, TextTZ
# Create your views here.
# Create your views here.
template_name = 'landpage/starter.html'
def index(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]---
    #template = loader.get_template('polls/index.html')
    #period = MyOption.objects.filter(active = 1)
    #period_on = 'all'
    #for per in period:
    #    period_on = per.text
    #df_text = list(TextForMMMF.objects.filter(Q(period_on='all')|Q(period_on = period_on)))
    lang = chooseLang(request)
    print(lang)
    df_text = TextTZ.objects.filter(active = 1, lang = lang)
    #print(df_text)
    buf = {}
    for item in df_text:
        buf[item.text_name] = item.text

    #for item in df_text:
    #    buf[item.text_name] = item.text
    #buf['link_register'] = OptionsMMMF.objects.filter(name = 'link_register')[0].text
    buf['teachers_list'] = TeachersTZ.objects.filter(active = 1, lang = lang).order_by('orderindex')
    buf['teachers_list_main'] = TeachersTZ.objects.filter(active = 2, lang = lang).order_by('orderindex')
    buf['teachers_list_main3'] = TeachersTZ.objects.filter(active = 3, lang = lang).order_by('orderindex')
    en_un = University.objects.filter(active = 1)
    buf['eng_sum'] = sum([el.number for el in en_un])
    buf['university_list'] = en_un.order_by('orderindex')
    usa_un = University.objects.filter(active = 2)
    buf['usa_sum'] = sum([el.number for el in usa_un])
    buf['university_list2'] = usa_un.order_by('orderindex')
    context = buf
    context['local_template'] = 'landpage/index.html'
    context['lang']=lang
    
    form, success_message, error_message = emailView(request)
    buf['form'] = form
    buf['success_message'] = success_message
    buf['error_message'] = error_message

    return render(request, template_name, context)

def chooseLang(request):
    if 'language' in request.session:
        lang = request.session['language']
    else:
        lang = 'rus'
        
    if request.method == 'POST':
        if 'rus' in request.POST:
            lang = 'rus'
        elif 'eng' in request.POST:
            lang = 'eng'
            
    request.session['language'] = lang   
    return lang

def emailView(request):
    success_message = ''
    error_message = ''
    if request.method == 'POST':
        if 'phone' in request.POST:
            form = ContactForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                #subject = form.cleaned_data['subject']
                #from_email = form.cleaned_data['from_email']
                #message = form.cleaned_data['message']
                user = Contact(name=name)#, subject=subject, from_email = from_email, message = message)
                user.save()
                success_message = 'Мы скоро вам перезвоним. Спасибо!'
    
                subject = 'EdEra'
                message1 = "Здравствуйте, \n\nНаставник свяжется с Вами в ближайшее время!\n\n"
                message1 += "С уважением,\nКоманда EdEra"
    
                subject2 = "EdEra - новый клиент {}".format(name)
                message2 = "{}\n".format(name)#, from_email)
                #message2 += subject + "\n\n" + message
    
    
                try:
                    #send_mail(subject, message1, "info@edera-school.com", [from_email]) "taratuta.alexander@outlook.com"
                    send_mail(subject2, message2, "info@edera-school.com", ["aleksandr.taratuta@phystech.edu"])
                except Exception as e:
                    print(e)
                    pass
            else:
                error_message = 'В форме есть ошибки'
    form = ContactForm()
    return form, success_message, error_message