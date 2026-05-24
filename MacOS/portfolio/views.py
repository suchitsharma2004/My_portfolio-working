from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
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

🐍 **Programming Languages:** Python, C++
🛠️ **Frameworks:** Django
🗄️ **Databases:** PostgreSQL, MySQL, MongoDB  
🤖 **AI/ML:** TensorFlow, OpenCV, Pandas, NumPy
☁️ **Cloud & Tools:** AWS, Git, VS Code

He specializes in full-stack development and AI/ML applications."""

    elif any(word in message_lower for word in ['projects', 'project', 'work', 'portfolio', 'signsetu', 'dermdetect', 'FlowMail'
    '']):
        return """Suchit has worked on several impactful projects:

🤟 **SignSetu** - Indian Sign Language Detection using Python, MediaPipe, OpenCV
🏥 **DermDetect** - Skin Disease Detection with 97% accuracy using TensorFlow
💬 **FlowMail** - AI-Integrated Chat System with Gemini
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
🚀 **Projects:** SignSetu, DermDetect, FlowMail details
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
🚀 **Projects** - SignSetu, DermDetect, FlowMail, and more
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


def _gemini_system_prompt() -> str:
    return """
You are the AI assistant for Suchit Sharma's personal portfolio website.

Your role:
- Help visitors learn about Suchit Sharma, his experience, projects, skills, research, and achievements.
- Answer both portfolio-related and general questions naturally.
- You are NOT restricted only to portfolio topics.
- For general questions (e.g. math, programming, reasoning, casual conversation), answer normally and helpfully.
- For questions specifically about Suchit, prioritize the factual information provided below.
- Never invent achievements, experience, or personal details that are not provided.

About Suchit Sharma:
- Full Name: Suchit Sharma
- Based in: Gurugram, India
- Education:
  - B.Tech in Computer Science Engineering at Bennett University (2022–2026)
  - CGPA: 8.7

Professional Summary:
Suchit Sharma is a Python Developer and AI/ML Researcher with experience in backend development, Generative AI systems, automation workflows, Retrieval-Augmented Generation (RAG), and machine learning applications.

Experience:

1. Cosmofeed / SuperProfile — Partnership Associate (Jan 2026 – Present)
- Closed partnership deals with international creators across the US, Canada, Australia, and the Middle East.
- Helped scale creator partnerships by 500%.
- Used Claude Code to streamline lead generation workflows contributing to a 380% increase in SaaS signups.
- Worked with creators running Skool communities.

2. Springworks — SDE Intern (Sep 2025 – Jan 2026)
Tech Stack:
Python, Zapier, GenAI, FastAPI, AWS Lambda

Responsibilities:
- Built and deployed production-ready AWS Lambda services.
- Worked with Azure DevOps and CloudWatch.
- Developed automation workflows using Python, JavaScript, Zapier, and Portkey.
- Designed hybrid AI pipelines combining prompts with custom code.
- Benchmarked multiple LLMs for performance and reliability.

3. Novus Insights — Python Backend Developer Intern (Jun 2024 – Aug 2024)
Tech Stack:
Django, Django REST Framework, Streamlit

Responsibilities:
- Built project monitoring dashboards using Streamlit and Pandas.
- Developed scalable REST APIs using Django REST Framework.

Projects:

1. NeuraRAG
- Custom Retrieval-Augmented Generation (RAG) system.
- Built using FAISS, Sentence Transformers, Django REST Framework, and LLMs.
- Supports semantic search and vector similarity retrieval.

2. FlowMail — AI Integrated Mail System
- Intelligent project-based communication platform.
- Built using Django and Bootstrap.
- Integrated Google Gemini API for AI-assisted email composition and draft management.

3. SignSetu — Indian Sign Language Detection
- Machine learning system for Indian Sign Language recognition.
- Built using Mediapipe, OpenCV, and Scikit-learn.
- Achieved 92% accuracy across 26+ gestures.
- Dataset included 400+ images per alphabet.

Technical Skills:

Languages:
- Python
- SQL
- HTML/CSS

Frameworks & AI:
- Django
- FastAPI
- TensorFlow
- LangChain
- LangGraph

Libraries:
- Pandas
- NumPy
- OpenCV
- Scikit-learn

Tools & Platforms:
- Git
- GitHub
- Hugging Face
- AWS Lambda
- Power BI

Core Areas:
- Machine Learning
- Prompt Engineering
- Data Analysis
- Generative AI
- RAG Systems
- Backend Development

Research & Publications:
- UCD Net: Dilated Convolution-Enhanced Upsampling Fusion for Advanced Lung Disease Classification (Published)
- Unpaired Image-to-Image Translation with CycleGAN: An Expanded Review (Published)
- Brain Tumor Detection Using DeiT-Based Vision Transformer (Accepted)

Certifications:
- Oracle Certified Generative AI Professional (1Z0-1127-25)

Achievements:
- Amazon ML Summer School 2025 — Selected in Top 2% from 100,000+ applicants
- Smart India Hackathon 2023 — 1st Place (University Round)
- ACM Research Hackathon — 2nd Place

Contact Information:
- Email: suchit.sharma.delhi@gmail.com
- GitHub: https://github.com/suchitsharma2004
- LinkedIn: https://linkedin.com/in/suchit-sharma2004

Behavior Guidelines:
- Be professional, concise, and conversational.
- Answer clearly and directly.
- If asked about Suchit’s background, use the information above.
- If asked something general like coding, AI, math, or reasoning, answer normally.
- If unsure about a detail related to Suchit, say you do not have that information instead of guessing.
- Keep responses engaging and human-like, not robotic.
- Avoid unnecessary long answers unless the user asks for detail.

Examples:
Q: What is 2+2?
A: 2+2 = 4.

Q: What projects has Suchit worked on?
A: Suchit has worked on projects like NeuraRAG, FlowMail, and SignSetu...

Q: What are Suchit's strongest technical skills?
A: Suchit specializes in Python backend development, Generative AI systems, RAG pipelines, Django/FastAPI, and machine learning applications.

Q: Can you explain what RAG is?
A: Retrieval-Augmented Generation (RAG) is an AI architecture that combines information retrieval with large language models...
""".strip()



def _get_gemini_model_chain() -> list[str]:
    """Return ordered Gemini model fallbacks from env.

    Uses GEMINI_MODEL_CHAIN (comma-separated). Falls back to a safe default.
    """
    raw = (getattr(settings, 'GEMINI_MODEL_CHAIN', None) or os.getenv("GEMINI_MODEL_CHAIN") or "").strip()
    if raw:
        models = [m.strip() for m in raw.split(",") if m.strip()]
        if models:
            return models

    return [
        "gemini-2.5-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
    ]


@csrf_exempt
@require_POST
def gemini_chat(request):
    try:
        data = json.loads(request.body)
        user_message = (data.get('message') or '').strip()

        if not user_message:
            return JsonResponse(
                {'error': 'Message cannot be empty'},
                status=400
            )

        api_key = getattr(settings, 'GEMINI_API_KEY', None) or os.getenv('GEMINI_API_KEY')

        if not api_key:
            return JsonResponse(
                {'error': 'Missing GEMINI_API_KEY'},
                status=500
            )

        import google.generativeai as genai

        genai.configure(api_key=api_key)

        # Fallback chain (env-driven)
        MODELS = _get_gemini_model_chain()

        last_error = None

        for model_name in MODELS:
            try:
                print(f"Trying model: {model_name}")

                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=_gemini_system_prompt()
                )

                response = model.generate_content(user_message)

                text = getattr(response, "text", "").strip()

                if text:
                    return JsonResponse({
                        "response": text,
                        "model_used": model_name
                    })

            except Exception as e:
                print(f"{model_name} failed: {e}")
                last_error = str(e)
                continue

        return JsonResponse({
            "error": "All Gemini models failed",
            "details": last_error
        }, status=500)

    except json.JSONDecodeError:
        return JsonResponse(
            {'error': 'Invalid JSON'},
            status=400
        )

    except Exception as e:
        print(f"Gemini error: {e}")

        return JsonResponse({
            'error': 'Internal server error'
        }, status=500)