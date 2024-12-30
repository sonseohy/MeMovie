<template>
  <div class="chatbot-container">
    <div class="chatbot-header">
      <h4>챗봇</h4>
      <button @click="closeChatbot" class="close-btn">X</button>
    </div>
    <div class="chatbot-messages">
      <div class="message" v-for="(message, index) in messages" :key="index">
        <div :class="message.sender === 'bot' ? 'bot-message' : 'user-message'">
          {{ message.text }}
        </div>
      </div>
    </div>
    <div class="chatbot-input">
      <input v-model="userMessage" @keyup.enter="sendMessage" placeholder="메시지를 입력하세요..." />
      <button @click="sendMessage">전송</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  isVisible: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(['update:isVisible']);

const userMessage = ref('');
const messages = ref([
  { sender: 'bot', text: '안녕하세요! 무엇을 도와드릴까요?' },
]);

const sendMessage = () => {
  if (userMessage.value.trim() === '') return;

  // 사용자 메시지 추가
  messages.value.push({ sender: 'user', text: userMessage.value });

  // 봇의 응답 (여기서는 간단한 예시로 고정된 메시지)
  messages.value.push({ sender: 'bot', text: '제가 도와드릴 수 있는 일이 있나요?' });

  // 입력창 초기화
  userMessage.value = '';
};

const closeChatbot = () => {
  emit('update:isVisible', false);
};
</script>

<style scoped>
.chatbot-container {
  position: fixed;
  bottom: -800px;
  left: 10px; /* right에서 left로 변경 */
  width: 300px;
  max-width: 100%;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 999;
  padding: 10px;
}


.chatbot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.close-btn {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
}

.chatbot-messages {
  max-height: 300px;
  overflow-y: auto;
  margin-top: 10px;
}

.message {
  margin: 5px 0;
}

.bot-message {
  background-color: #f1f1f1;
  padding: 8px;
  border-radius: 5px;
}

.user-message {
  background-color: #4caf50;
  color: white;
  padding: 8px;
  border-radius: 5px;
  text-align: right;
}

.chatbot-input {
  display: flex;
  margin-top: 10px;
}

.chatbot-input input {
  flex-grow: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.chatbot-input button {
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 8px;
  margin-left: 5px;
  cursor: pointer;
}

.chatbot-input button:hover {
  background-color: #45a049;
}
</style>
