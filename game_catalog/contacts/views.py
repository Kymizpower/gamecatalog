from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, '✅ Ваше сообщение успешно отправлено! Мы ответим вам в ближайшее время.')
                return redirect('contacts')
            except Exception as e:
                messages.error(request, f'❌ Произошла ошибка при отправке сообщения: {str(e)}')
        else:
            messages.error(request, '❌ Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'page_title': 'Контакты',
        'page_description': 'Свяжитесь с нами любым удобным способом. Мы всегда рады помочь!',
    }
    
    return render(request, 'contacts/contacts.html', context)