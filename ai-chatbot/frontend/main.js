// Updated sendMessage function with secure backend API
async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    
    // Add user message
    addMessage(message, true);
    chatInput.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        // Secure API call to backend
        const response = await fetch('http://localhost:5001/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        // Hide typing indicator
        hideTypingIndicator();
        
        // Add bot response
        if (data.response) {
            addMessage(data.response);
            
            // Highlight emergency responses
            if (data.emergency) {
                const lastMessage = chatBody.lastChild;
                lastMessage.style.background = 'linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%)';
                lastMessage.style.borderLeft = '4px solid #f44336';
            }
        } else {
            addMessage('ขออภัย เกิดข้อผิดพลาดในการประมวลผล: ' + data.error);
        }
    } catch (error) {
        hideTypingIndicator();
        
        // Enhanced fallback responses
        const fallbackResponses = [
            "ขออภัยในความไม่สะดวก ขณะนี้ระบบมีปัญหา ช่วยลองใหม่อีกครั้งหรือโทรสอบถามที่ 012-345-6789",
            "สวัสดีค่ะ! ขณะนี้ระบบกำลังปรับปรุง ช่วยลองใหม่อีกครั้งหรือติดต่อแผนกผู้ป่วยใน 012-345-6789",
            "ข้อมูลสุขภาพเบื้องต้น: พักผ่อนให้เพียงพอ ดื่มน้ำวันละ 8-10 แก้ว และรับประทานอาหารมีประโยชน์",
            "หากมีอาการไม่สบายรุนแรง กรุณาติดต่อแผนกฉุกเฉินที่ 012-345-6790 ตลอด 24 ชั่วโมง"
        ];
        
        const randomResponse = fallbackResponses[Math.floor(Math.random() * fallbackResponses.length)];
        addMessage(randomResponse);
    }
}

// Enhanced error handling
function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    avatarDiv.textContent = isUser ? 'คุณ' : '🏥';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = content; // Allow basic HTML for formatting
    
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    chatBody.appendChild(messageDiv);
    
    // Scroll to bottom
    chatBody.scrollTop = chatBody.scrollHeight;
}