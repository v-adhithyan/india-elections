from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

from .constants import GOOGLE_RECAPTCHA_SITE_KEY
from .forms import OpinionPollForm
from .models import Constituency, IFrameEnabledSites
from .utils import get_ip_address, verify_recaptcha


@csrf_exempt
@xframe_options_exempt
def opinion_poll(request):
    get_object_or_404(IFrameEnabledSites, domain=request.META["HTTP_HOST"], enabled=True)

    form = OpinionPollForm()

    if request.method == "POST":
        form = OpinionPollForm(request.POST)

        if form.is_valid() and verify_recaptcha(request):
            try:
                voter = form.save(commit=False)
                voter.ip_address = get_ip_address(request)
                voter.save()
                messages.success(request, 'Your opinion was saved. Results will be published on May 3rd week.')
            except Exception:
                messages.error(request, "Unable to save your opinion. Please try again after some time.")

    return render(
        request,
        template_name='poll.html',
        context={
            'form': form,
            'google_recaptcha_site_key': GOOGLE_RECAPTCHA_SITE_KEY})

@csrf_exempt
def load_constituencies(request):
    state_id = request.GET.get('state')
    constituencies = Constituency.objects.filter(state_union_id=state_id).order_by('name')
    return render(request, 'places.html', {'places': constituencies})
