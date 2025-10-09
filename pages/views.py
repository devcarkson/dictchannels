from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from testimonials.models import Testimonial
from services.models import Service
from courses.models import Course
from events.models import Event
from .models import (
    Student, TeamMember, ContactSubmission, NewsletterSubscription,
    QuoteSubmission, ServiceInquiry, Enrollment, Assignment,
    AssignmentSubmission, Certificate, Announcement, Message, Payment
)
from .forms import ContactForm, NewsletterForm, QuoteForm, ServiceInquiryForm, StudentProfileForm, StudentRegistrationForm

def home(request):
    testimonials = Testimonial.objects.all()
    services = Service.objects.all()
    newsletter_form = NewsletterForm()
    courses = Course.objects.all()
    context = {
        'testimonials': testimonials,
        'services': services,
        'courses': courses,
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/home.html', context)

def about(request):
    newsletter_form = NewsletterForm()
    context = {
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/about.html', context)

def services(request):
    if request.method == 'POST':
        form = ServiceInquiryForm(request.POST)
        if form.is_valid():
            # Save service inquiry to database
            service_inquiry = form.save()

            # Send email notification to admin
            try:
                subject = f'New Service Inquiry from {service_inquiry.name}'
                message = f"""
New service inquiry received:

Name: {service_inquiry.name}
Email: {service_inquiry.email}
Phone: {service_inquiry.phone}
Service: {service_inquiry.service}

Message:
{service_inquiry.message}

Submitted at: {service_inquiry.submitted_at}
                """
                from_email = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@d-ictchannels.com'
                recipient_list = [settings.ADMIN_EMAIL] if hasattr(settings, 'ADMIN_EMAIL') else ['carksonniit@gmail.com']

                send_mail(
                    subject,
                    message,
                    from_email,
                    recipient_list,
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email notification failed: {e}")

            messages.success(request, 'Your service inquiry has been submitted successfully! We will get back to you soon.')
            return redirect('services')
    else:
        form = ServiceInquiryForm()

    services = Service.objects.all()
    newsletter_form = NewsletterForm()
    context = {
        'services': services,
        'newsletter_form': newsletter_form,
        'form': form,
    }
    return render(request, 'pages/services.html', context)

def courses(request):
    courses = Course.objects.all()
    newsletter_form = NewsletterForm()
    context = {
        'courses': courses,
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/courses.html', context)

def courses_topup(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Top Up Programs',
        'page_subtitle': 'Advance Your Education',
        'page_content': '<p>The Top Up program is a 2-year program with 4 semesters that leads to a BSc Degree. Perfect for students looking to advance their education and career prospects.</p><p><strong>Duration:</strong> 2 years (4 semesters)<br><strong>Degree:</strong> BSc in Computer Science/IT<br><strong>Mode:</strong> Full-time/Part-time available</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'courses/topup.html', context)

def courses_diploma(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Diploma Programs',
        'page_subtitle': '6 Months Intensive Training',
        'page_content': '<p>The Diploma program is a 6-month intensive course that enables students to specialize in any IT skills field. Comprehensive training with hands-on projects.</p><p><strong>Duration:</strong> 6 months<br><strong>Focus:</strong> Specialized IT skills<br><strong>Projects:</strong> Real-world applications</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'courses/diploma.html', context)

def courses_certificate(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Certificate Programs',
        'page_subtitle': '1-4 Months Skill Development',
        'page_content': '<p>The Certificate program ranges from 1 to 4 months duration for students wanting to have skills in the IT field. Flexible durations to match your learning pace.</p><p><strong>Duration:</strong> 1-4 months<br><strong>Skills:</strong> Core IT competencies<br><strong>Certification:</strong> Industry-recognized certificates</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'courses/certificate.html', context)

def courses_school(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Tech 4 Schools Programs',
        'page_subtitle': 'IT Education for Young Minds',
        'page_content': '<p>The Tech 4 Schools program is designed for students in grades 1-12 to enable them to have IT skills. Age-appropriate curriculum for young learners.</p><p><strong>Age Group:</strong> Grades 1-12<br><strong>Focus:</strong> Basic to advanced computing skills<br><strong>Methodology:</strong> Interactive and fun learning</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'courses/school.html', context)

def courses_siwes(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'SIWES Programs',
        'page_subtitle': 'Industrial Training for Students',
        'page_content': '<p>The SIWES program is for students at higher institutions to give them professional IT skills. Mandatory industrial training with practical exposure.</p><p><strong>Target:</strong> Higher institution students<br><strong>Duration:</strong> 6 months<br><strong>Focus:</strong> Professional IT skills development</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'courses/siwes.html', context)

def courses_corporate(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Corporate Programs',
        'page_subtitle': 'Training for Organizations',
        'page_content': '<p>The Corporate program is for organizations that want to train their staff in professional IT skills. Customized training solutions for businesses.</p><p><strong>Target:</strong> Corporate organizations<br><strong>Customization:</strong> Tailored to company needs<br><strong>Delivery:</strong> On-site or online</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'courses/corporate.html', context)

def courses_customized(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Customized Programs',
        'page_subtitle': 'Bespoke Training Solutions',
        'page_content': '<p>The Customized program is for students who want to bring their course outline in IT to be taught. Fully customizable curriculum based on your requirements.</p><p><strong>Flexibility:</strong> Custom course outlines<br><strong>Content:</strong> Client-specified topics<br><strong>Delivery:</strong> As per client preference</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'courses/customized.html', context)

def events(request):
    events = Event.objects.all()
    newsletter_form = NewsletterForm()
    context = {
        'events': events,
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/events.html', context)

def contact(request):
    if request.method == 'POST':
        # Get form data from POST request
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Validate required fields
        if not all([fname, email, phone, subject, message]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('contact')

        # Save contact submission to database
        contact_submission = ContactSubmission.objects.create(
            fname=fname,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )

        # Send email notification to admin
        try:
            email_subject = f'New Contact Form Submission from {contact_submission.fname}'
            email_message = f"""
New contact form submission received:

Name: {contact_submission.fname}
Email: {contact_submission.email}
Phone: {contact_submission.phone}
Subject: {contact_submission.subject}

Message:
{contact_submission.message}

Submitted at: {contact_submission.submitted_at}
            """
            from_email = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@d-ictchannels.com'
            recipient_list = [settings.ADMIN_EMAIL] if hasattr(settings, 'ADMIN_EMAIL') else ['admin@d-ictchannels.com']

            send_mail(
                email_subject,
                email_message,
                from_email,
                recipient_list,
                fail_silently=True,
            )
        except Exception as e:
            print(f"Email notification failed: {e}")

        messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
        return redirect('contact')

    newsletter_form = NewsletterForm()
    context = {
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/contact.html', context)

def team(request):
    team_members = TeamMember.objects.filter(is_active=True)
    newsletter_form = NewsletterForm()
    context = {
        'team_members': team_members,
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/team.html', context)

def testimonial(request):
    testimonials = Testimonial.objects.all()
    newsletter_form = NewsletterForm()
    context = {
        'testimonials': testimonials,
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/testimonial.html', context)

def bank(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Bank Account Details',
        'page_subtitle': 'Payment Information',
        'page_content': '''
        <p>For your convenience, here are our bank account details for course payments and other transactions.</p>
        <div class="row g-4">
            <div class="col-lg-6">
                <div class="bg-light p-4 rounded">
                    <h5>Bank Name: Access Bank PLC</h5>
                    <p><strong>Account Name:</strong> D-ICT CHANNELS</p>
                    <p><strong>Account Number:</strong> 1234567890</p>
                    <p><strong>Account Type:</strong> Current Account</p>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="bg-light p-4 rounded">
                    <h5>Bank Name: Zenith Bank PLC</h5>
                    <p><strong>Account Name:</strong> D-ICT CHANNELS</p>
                    <p><strong>Account Number:</strong> 0987654321</p>
                    <p><strong>Account Type:</strong> Current Account</p>
                </div>
            </div>
        </div>
        <div class="mt-4">
            <p><strong>Note:</strong> Please include your full name and course name in the payment description for easy identification.</p>
        </div>
        ''',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/bank.html', context)

def branches(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Our Branches',
        'page_subtitle': 'Locations Across Nigeria',
        'page_content': '''
        <p>D-ICT CHANNELS has multiple training centers across Nigeria to serve you better.</p>
        <div class="row g-4">
            <div class="col-lg-6">
                <div class="bg-light p-4 rounded">
                    <h5>🏢 Lagos Branch (Head Office)</h5>
                    <p>2, Martins Street Off Ojuelegba Road, Yaba, Lagos State</p>
                    <p><strong>Phone:</strong> +234 8032867212, +234 8082171242</p>
                    <p><strong>Email:</strong> info@d-ictchannels.com</p>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="bg-light p-4 rounded">
                    <h5>🏢 Abuja Branch</h5>
                    <p>Suite 123, Wuse 2, Abuja, FCT</p>
                    <p><strong>Phone:</strong> +234 8032867213</p>
                    <p><strong>Email:</strong> abuja@d-ictchannels.com</p>
                </div>
            </div>
        </div>
        ''',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/branches.html', context)

def career(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Career Opportunities',
        'page_subtitle': 'Join Our Team',
        'page_content': '''
        <p>We're always looking for talented individuals to join our growing team. If you're passionate about technology education and software development, we want to hear from you!</p>
        <div class="row g-4">
            <div class="col-lg-6">
                <div class="bg-light p-4 rounded">
                    <h5>👨‍🏫 Senior Instructor</h5>
                    <p>Requirements: 3+ years teaching experience, expertise in Python/Java/C#</p>
                    <p><strong>Location:</strong> Lagos, Nigeria</p>
                    <p><strong>Type:</strong> Full-time</p>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="bg-light p-4 rounded">
                    <h5>💻 Software Developer</h5>
                    <p>Requirements: 2+ years development experience, React/Django knowledge</p>
                    <p><strong>Location:</strong> Lagos, Nigeria</p>
                    <p><strong>Type:</strong> Full-time</p>
                </div>
            </div>
        </div>
        <div class="mt-4">
            <p><strong>To apply:</strong> Send your CV and cover letter to careers@dictchannels.com</p>
        </div>
        ''',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/career.html', context)

def faq(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Frequently Asked Questions',
        'page_subtitle': 'Your Questions Answered',
        'page_content': '''
        <div class="accordion" id="faqAccordion">
            <div class="accordion-item">
                <h2 class="accordion-header" id="heading1">
                    <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse1" aria-expanded="true" aria-controls="collapse1">
                        What courses do you offer?
                    </button>
                </h2>
                <div id="collapse1" class="accordion-collapse collapse show" aria-labelledby="heading1" data-bs-parent="#faqAccordion">
                    <div class="accordion-body">
                        We offer a wide range of IT courses including Python, Java, C#, Web Development, Data Science, Cybersecurity, and many more.
                    </div>
                </div>
            </div>
            <div class="accordion-item">
                <h2 class="accordion-header" id="heading2">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse2" aria-expanded="false" aria-controls="collapse2">
                        Do you offer online classes?
                    </button>
                </h2>
                <div id="collapse2" class="accordion-collapse collapse" aria-labelledby="heading2" data-bs-parent="#faqAccordion">
                    <div class="accordion-body">
                        Yes, we offer both online and in-person training options to suit your schedule and learning preferences.
                    </div>
                </div>
            </div>
            <div class="accordion-item">
                <h2 class="accordion-header" id="heading3">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse3" aria-expanded="false" aria-controls="collapse3">
                        What are your payment options?
                    </button>
                </h2>
                <div id="collapse3" class="accordion-collapse collapse" aria-labelledby="heading3" data-bs-parent="#faqAccordion">
                    <div class="accordion-body">
                        We accept bank transfers, online payments, and installment plans. Contact us for detailed payment information.
                    </div>
                </div>
            </div>
        </div>
        ''',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/faq.html', context)

def software(request):
    newsletter_form = NewsletterForm()
    context = {
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/software.html', context)

def training(request):
    newsletter_form = NewsletterForm()
    context = {
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/training.html', context)

def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('subemail')

        if not email:
            messages.error(request, 'Please enter a valid email address.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))

        # Check if email already exists
        if NewsletterSubscription.objects.filter(email=email).exists():
            messages.info(request, 'You are already subscribed to our newsletter.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))

        # Save newsletter subscription
        NewsletterSubscription.objects.create(email=email)
        messages.success(request, 'Thank you for subscribing to our newsletter!')
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    # If not POST, redirect to home
    return redirect('home')

def digital(request):
    newsletter_form = NewsletterForm()
    context = {
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/digital.html', context)

def admission(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'International University Admission',
        'page_subtitle': 'Your Gateway to Global Education',
        'page_content': '''
        <p>We help students secure admission from different countries to apply for and enroll in higher education abroad, including America, Canada, UK, and more.</p>
        <div class="row g-4">
            <div class="col-lg-6">
                <div class="bg-light p-4 rounded">
                    <h5>🎓 University Applications</h5>
                    <p>Complete application assistance for top universities worldwide.</p>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="bg-light p-4 rounded">
                    <h5>📋 Visa Processing</h5>
                    <p>Guidance and support for student visa applications.</p>
                </div>
            </div>
        </div>
        <div class="mt-4">
            <h5>Countries We Support:</h5>
            <ul>
                <li>United States of America</li>
                <li>United Kingdom</li>
                <li>Canada</li>
                <li>Australia</li>
                <li>Germany</li>
            </ul>
        </div>
        ''',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/admission.html', context)

def quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            # Save quote submission to database
            quote_submission = form.save()

            # Send email notification to admin
            try:
                subject = f'New Quote Request from {quote_submission.name}'
                message = f"""
New quote request received:

Name: {quote_submission.name}
Email: {quote_submission.email}
Phone: {quote_submission.phone}
Service: {quote_submission.service}

Project Description:
{quote_submission.message}

Submitted at: {quote_submission.submitted_at}
                """
                from_email = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@d-ictchannels.com'
                recipient_list = [settings.ADMIN_EMAIL] if hasattr(settings, 'ADMIN_EMAIL') else ['admin@d-ictchannels.com']

                send_mail(
                    subject,
                    message,
                    from_email,
                    recipient_list,
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email notification failed: {e}")

            messages.success(request, 'Your quote request has been submitted successfully! We will get back to you soon.')
            return redirect('quote')
    else:
        form = QuoteForm()

    newsletter_form = NewsletterForm()
    context = {
        'newsletter_form': newsletter_form,
        'form': form,
    }
    return render(request, 'pages/quote.html', context)

def topup(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Top Up Programs',
        'page_subtitle': 'Advance Your Education',
        'page_content': '<p>The Top Up program is a 2-year program with 4 semesters that leads to a BSc Degree. Perfect for students looking to advance their education and career prospects.</p><p><strong>Duration:</strong> 2 years (4 semesters)<br><strong>Degree:</strong> BSc in Computer Science/IT<br><strong>Mode:</strong> Full-time/Part-time available</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/topup.html', context)

def diploma(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Diploma Programs',
        'page_subtitle': '6 Months Intensive Training',
        'page_content': '<p>The Diploma program is a 6-month intensive course that enables students to specialize in any IT skills field. Comprehensive training with hands-on projects.</p><p><strong>Duration:</strong> 6 months<br><strong>Focus:</strong> Specialized IT skills<br><strong>Projects:</strong> Real-world applications</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/diploma.html', context)

def certificate(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Certificate Programs',
        'page_subtitle': '1-4 Months Skill Development',
        'page_content': '<p>The Certificate program ranges from 1 to 4 months duration for students wanting to have skills in the IT field. Flexible durations to match your learning pace.</p><p><strong>Duration:</strong> 1-4 months<br><strong>Skills:</strong> Core IT competencies<br><strong>Certification:</strong> Industry-recognized certificates</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/certificate.html', context)

def school(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Tech 4 Schools Programs',
        'page_subtitle': 'IT Education for Young Minds',
        'page_content': '<p>The Tech 4 Schools program is designed for students in grades 1-12 to enable them to have IT skills. Age-appropriate curriculum for young learners.</p><p><strong>Age Group:</strong> Grades 1-12<br><strong>Focus:</strong> Basic to advanced computing skills<br><strong>Methodology:</strong> Interactive and fun learning</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/school.html', context)

def siwes(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'SIWES Programs',
        'page_subtitle': 'Industrial Training for Students',
        'page_content': '<p>The SIWES program is for students at higher institutions to give them professional IT skills. Mandatory industrial training with practical exposure.</p><p><strong>Target:</strong> Higher institution students<br><strong>Duration:</strong> 6 months<br><strong>Focus:</strong> Professional IT skills development</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/siwes.html', context)

def internship(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Internship Programs',
        'page_subtitle': 'Learn and Work Experience',
        'page_content': '<p>The Internship program is for students who want to learn and also have working experience in an IT firm. Combines learning with practical work experience.</p><p><strong>Duration:</strong> 3-6 months<br><strong>Experience:</strong> Real workplace exposure<br><strong>Skills:</strong> Professional development</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/internship.html', context)

def corporate(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Corporate Programs',
        'page_subtitle': 'Training for Organizations',
        'page_content': '<p>The Corporate program is for organizations that want to train their staff in professional IT skills. Customized training solutions for businesses.</p><p><strong>Target:</strong> Corporate organizations<br><strong>Customization:</strong> Tailored to company needs<br><strong>Delivery:</strong> On-site or online</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/corporate.html', context)

def customized(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Customized Programs',
        'page_subtitle': 'Bespoke Training Solutions',
        'page_content': '<p>The Customized program is for students who want to bring their course outline in IT to be taught. Fully customizable curriculum based on your requirements.</p><p><strong>Flexibility:</strong> Custom course outlines<br><strong>Content:</strong> Client-specified topics<br><strong>Delivery:</strong> As per client preference</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/customized.html', context)

def mode(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Mode of Training',
        'page_subtitle': 'Flexible Learning Options',
        'page_content': '<p>We offer various modes of training to suit different learning preferences and schedules. Choose the option that works best for you.</p><div class="row g-4"><div class="col-lg-4"><div class="bg-light p-4 rounded text-center"><i class="fas fa-building fa-3x text-primary mb-3"></i><h5>Classroom Training</h5><p>Traditional classroom learning with instructors.</p></div></div><div class="col-lg-4"><div class="bg-light p-4 rounded text-center"><i class="fas fa-laptop fa-3x text-primary mb-3"></i><h5>Online Training</h5><p>Virtual learning from anywhere, anytime.</p></div></div><div class="col-lg-4"><div class="bg-light p-4 rounded text-center"><i class="fas fa-blender-phone fa-3x text-primary mb-3"></i><h5>Hybrid Training</h5><p>Combination of online and classroom learning.</p></div></div></div>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/mode.html', context)

def fast(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Fast Track Programs',
        'page_subtitle': 'Accelerated Learning Paths',
        'page_content': '<p>Fast-track programs are accelerated learning paths designed to help individuals gain specific skills or qualifications in a shorter time frame.</p><p><strong>Duration:</strong> 2-8 weeks intensive<br><strong>Focus:</strong> Specific skill sets<br><strong>Intensity:</strong> Full-time training</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/fast.html', context)

def seminar(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Monthly Seminar',
        'page_subtitle': 'Knowledge Sharing Sessions',
        'page_content': '<p>Our Monthly Seminar is designed to provide valuable insights, knowledge, and networking opportunities for professionals and students alike.</p><p><strong>Frequency:</strong> Monthly<br><strong>Topics:</strong> Current IT trends and technologies<br><strong>Format:</strong> Interactive sessions</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/seminar.html', context)

def workshop(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Monthly Workshop',
        'page_subtitle': 'Hands-on Learning Experience',
        'page_content': '<p>Our Monthly Workshop offers hands-on, practical training sessions designed to help you develop new skills and gain practical experience.</p><p><strong>Frequency:</strong> Monthly<br><strong>Activities:</strong> Practical exercises and projects<br><strong>Duration:</strong> Full-day sessions</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/workshop.html', context)

def scholarship(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Quarterly Scholarship',
        'page_subtitle': 'Financial Support for Education',
        'page_content': '<p>Our Quarterly Scholarship program is designed to support and empower students by providing financial assistance for their education.</p><p><strong>Frequency:</strong> Quarterly<br><strong>Benefits:</strong> Fee discounts and waivers<br><strong>Eligibility:</strong> Based on merit and need</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/scholarship.html', context)

def exams(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Certification Exams',
        'page_subtitle': 'Validate Your Skills',
        'page_content': '<p>We prepare students for various industry-recognized certification exams to validate their skills and enhance career prospects.</p><p><strong>Certifications:</strong> CompTIA, Cisco, Microsoft, Oracle<br><strong>Preparation:</strong> Comprehensive training and practice<br><strong>Success Rate:</strong> High pass rates</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/exams.html', context)

def blogs(request):
    newsletter_form = NewsletterForm()
    context = {
        'page_title': 'Latest Blog',
        'page_subtitle': 'Insights and Updates',
        'page_content': '<p>Check out our Latest Blog for fresh insights, expert tips, and in-depth discussions on the topics that matter most in technology and education.</p><p><strong>Topics:</strong> Technology trends, career advice, industry news<br><strong>Authors:</strong> Industry experts and instructors<br><strong>Updates:</strong> Regular posts and articles</p>',
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/blogs.html', context)

def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('un')  # email
        password = request.POST.get('pw')

        # Authenticate with email as username
        user = authenticate(request, username=email, password=password)

        if user is not None and isinstance(user, Student):
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid email or password.')

    newsletter_form = NewsletterForm()
    context = {
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/student_login.html', context)

@login_required
def student_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def student_dashboard(request):
    if not isinstance(request.user, Student):
        messages.error(request, 'Access denied. Student login required.')
        return redirect('student_login')

    # Get student's enrollments
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    enrolled_courses = enrollments.count()

    # Calculate average progress
    if enrolled_courses > 0:
        avg_progress = sum(e.progress_percentage for e in enrollments) // enrolled_courses
    else:
        avg_progress = 0

    # Get pending assignments
    pending_assignments = AssignmentSubmission.objects.filter(
        student=request.user,
        status__in=['pending', 'submitted']
    ).count()

    # Get certificates count
    certificates_count = Certificate.objects.filter(student=request.user).count()

    # Get recent enrollments (limit to 2 for display)
    recent_enrollments = enrollments.order_by('-enrolled_at')[:2]

    # Get recent activity (assignments and certificates)
    recent_submissions = AssignmentSubmission.objects.filter(
        student=request.user
    ).select_related('assignment').order_by('-submitted_at')[:3]

    recent_certificates = Certificate.objects.filter(
        student=request.user
    ).select_related('course').order_by('-issued_at')[:2]

    # Combine and sort recent activities
    activities = []
    for sub in recent_submissions:
        activities.append({
            'type': 'assignment',
            'title': f"Submitted: {sub.assignment.title}",
            'date': sub.submitted_at,
            'icon': 'fas fa-check-circle',
            'color': 'bg-success'
        })

    for cert in recent_certificates:
        activities.append({
            'type': 'certificate',
            'title': f"Earned Certificate: {cert.course.title}",
            'date': cert.issued_at,
            'icon': 'fas fa-certificate',
            'color': 'bg-warning'
        })

    # Sort activities by date
    activities.sort(key=lambda x: x['date'], reverse=True)
    recent_activities = activities[:5]

    # Get upcoming assignments (due in next 7 days)
    from django.utils import timezone
    from datetime import timedelta
    upcoming_assignments = Assignment.objects.filter(
        course__enrollments__student=request.user,
        due_date__gte=timezone.now(),
        due_date__lte=timezone.now() + timedelta(days=7)
    ).distinct().order_by('due_date')[:3]

    context = {
        'enrolled_courses': enrolled_courses,
        'avg_progress': avg_progress,
        'pending_assignments': pending_assignments,
        'certificates_count': certificates_count,
        'recent_enrollments': recent_enrollments,
        'recent_activities': recent_activities,
        'upcoming_assignments': upcoming_assignments,
    }
    return render(request, 'pages/student_dashboard.html', context)

@login_required
def edit_profile(request):
    if not isinstance(request.user, Student):
        messages.error(request, 'Access denied. Student login required.')
        return redirect('student_login')

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('student_dashboard')
    else:
        form = StudentProfileForm(instance=request.user)

    context = {
        'form': form,
    }
    return render(request, 'pages/edit_profile.html', context)

def student_register(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Registration successful! Your Student ID is {user.student_id}. Please login.')
            return redirect('student_login')
    else:
        form = StudentRegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'pages/student_register.html', context)