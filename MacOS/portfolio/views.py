from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.contrib import messages
import json
import ssl
import os
# Remove the ctransformers import to avoid model loading issues for now
# from ctransformers import AutoModelForCausalLM
import time

# Create your views here.
def home(request):
    return render(request, 'portfolio/home.html')

def projects(request):
    return render(request, 'portfolio/projects.html')

def contact(request):
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Validate required fields
        if not all([name, email, subject, message]):
            context = {
                'error': True,
                'message': 'Please fill in all required fields.'
            }
            return render(request, 'portfolio/contact.html', context)
        
        # Prepare email content
        email_subject = f"Portfolio Contact: {subject}"
        email_message = f"""
New contact form submission from your portfolio:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
This message was sent from your portfolio contact form.
        """
        
        try:
            # Send email using smtplib with custom SSL context for macOS
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            import ssl
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = settings.CONTACT_EMAIL
            msg['Subject'] = email_subject
            msg.attach(MIMEText(email_message, 'plain'))
            
            # Create SSL context that works with macOS
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            # Connect and send email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls(context=context)
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                text = msg.as_string()
                server.sendmail(settings.EMAIL_HOST_USER, settings.CONTACT_EMAIL, text)
            
            # Success response
            context = {
                'success': True,
                'message': 'Thank you for your message! I\'ll get back to you soon.'
            }
            
        except BadHeaderError as e:
            context = {
                'error': True,
                'message': 'Invalid header found. Please try again.'
            }
        except Exception as e:
            context = {
                'error': True,
                'message': 'Sorry, there was an error sending your message. Please try again later or contact me directly.'
            }
        
        return render(request, 'portfolio/contact.html', context)
    
    return render(request, 'portfolio/contact.html')

# Simplified LLM implementation - using fallback responses for now
# This avoids server crashes while providing intelligent responses

def get_fallback_response(user_message):
    """Provide intelligent responses based on keywords"""
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['skills', 'skill', 'technical', 'programming', 'languages', 'technology', 'tech']):
        return """Suchit Sharma has strong technical skills in:

🐍 **Programming Languages:** Python, C++, JavaScript
🛠️ **Frameworks:** Django, React, Node.js
🗄️ **Databases:** PostgreSQL, MySQL, MongoDB  
🤖 **AI/ML:** TensorFlow, OpenCV, Pandas, NumPy
☁️ **Cloud & Tools:** AWS, Docker, Git, VS Code

He specializes in full-stack development and AI/ML applications."""

    elif any(word in message_lower for word in ['projects', 'project', 'work', 'portfolio', 'signsetu', 'dermdetect', 'chatapp']):
        return """Suchit has worked on several impactful projects:

🤟 **SignSetu** - Indian Sign Language Detection using Python, MediaPipe, OpenCV
🏥 **DermDetect** - Skin Disease Detection with 97% accuracy using TensorFlow
💬 **ChatApp** - AI-Integrated Chat System with LLaMA 3.2
🌐 **Portfolio Website** - This interactive macOS-style interface

Each project demonstrates his expertise in combining AI/ML with practical applications."""

    elif any(word in message_lower for word in ['education', 'university', 'college', 'study', 'bennett', 'degree', 'score', 'marks']):
        return """Suchit Sharma is pursuing his Computer Science and Engineering degree (Data Science specialization) at Bennett University, Greater Noida. He's expected to graduate in 2026 with a strong CGPA of 8.70.

🎓 **Current:** CSE (Data Science) at Bennett University (2026)
📚 **CGPA:** 8.70
🏫 **School:** Shalom Hills International School (91% in Grade X, 90% in Grade XII)"""

    elif any(word in message_lower for word in ['experience', 'internship', 'work', 'job', 'company']):
        return """Suchit gained valuable industry experience as a Backend Developer Intern at Novus Insights (Jun-Aug 2024):

💼 **Role:** Backend Developer Intern
🏢 **Company:** Novus Insights
📅 **Duration:** Jun-Aug 2024

**Key Achievements:**
• Built real-time chat application using Django REST & Streamlit
• Created executive dashboard for project performance monitoring
• Developed and integrated APIs for ongoing projects"""

    elif any(word in message_lower for word in ['contact', 'reach', 'connect', 'social', 'github', 'linkedin']):
        return """You can connect with Suchit through:

🐙 **GitHub:** https://github.com/suchitsharma2004
💼 **LinkedIn:** https://linkedin.com/in/suchitsharma2004
📧 **Email:** Use the contact form in the Contact app on this portfolio

He's always open to discussing new opportunities, collaborations, or interesting tech projects!"""

    elif any(word in message_lower for word in ['achievements', 'awards', 'publications', 'hackathon', 'competition']):
        return """Suchit has impressive achievements and recognition:

🏆 **Competition Success:**
• 1st place in SIH 2023 (University round)
• 2nd place in ACM Research Hackathon

📄 **Publications:**
• Published: "UCD Net: Dilated Convolution-Enhanced Upsampling Fusion for Advanced Lung Disease Classification"
• Under Review: Brain Tumor Detection using Vision Transformers
• Under Review: Multimodal Emotion Recognition Research

👥 **Leadership:**
• Research Head, Computer Society of India (Sep 2023 – May 2024)
• Research Member, Artificial Intelligence Society"""

    elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings', 'who are you']):
        return """Hello! I'm Suchit Sharma's AI assistant. I can tell you everything about his skills, projects, education, and experience.

✨ **Try asking about:**
• His technical skills and programming languages
• His innovative projects like SignSetu and DermDetect  
• His education and achievements
• His work experience and internships
• How to contact him

What would you like to know about Suchit?"""

    elif any(word in message_lower for word in ['help', 'what can you do', 'commands']):
        return """I'm here to help you learn about Suchit Sharma! Here's what I can tell you about:

🛠️ **Skills:** Programming languages, frameworks, tools
🚀 **Projects:** SignSetu, DermDetect, ChatApp details
🎓 **Education:** Bennett University background
💼 **Experience:** Internship and work history
🏆 **Achievements:** Awards, publications, leadership
📞 **Contact:** How to reach Suchit

Just ask me naturally! For example:
• "What programming languages does Suchit know?"
• "Tell me about his projects"
• "What's his educational background?"
• "How can I contact him?"

You can also use built-in terminal commands: `clear`, `skills`, `projects`, `help`"""

    else:
        return f"""I'm Suchit Sharma's AI assistant! While I'd love to help with "{user_message}", I'm specifically designed to share information about Suchit's:

🎯 **Technical Skills** - Programming languages, frameworks, tools
🚀 **Projects** - SignSetu, DermDetect, ChatApp, and more
🎓 **Education** - CSE at Bennett University
💼 **Experience** - Backend development internship
🏆 **Achievements** - Awards, publications, leadership
📞 **Contact** - How to reach him

Feel free to ask about any of these topics! Try questions like:
• "What are his technical skills?"
• "Tell me about his projects"
• "What's his background?"
• "How can I contact him?" """

@csrf_exempt
@require_http_methods(["POST"])
def llm_chat(request):
    """Handle chat requests using intelligent fallback responses"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        print(f"💬 User message: {user_message}")
        
        # Use intelligent fallback response system
        ai_response = get_fallback_response(user_message)
        
        print(f"✅ Response generated successfully")
        
        return JsonResponse({
            'response': ai_response
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        print(f"Error in chat: {e}")
        return JsonResponse({
            'error': 'Sorry, I encountered an error processing your request. Please try again.'
        }, status=500)

@csrf_exempt
def llm_test(request):
    """Simple test endpoint for the chat system"""
    try:
        # Test fallback system
        fallback_response = get_fallback_response("hello")
        
        return JsonResponse({
            'fallback_response': fallback_response,
            'system_status': 'Intelligent response system active',
            'status': 'success'
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'status': 'error'
        }, status=500)