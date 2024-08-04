new Vue({
  el: '#app',
  data: {
    inputText: '',
    inputAudioUrl: '',
    virtualImage: 'default_image',
    background: 'default_background',
    requestId: null,
    progress: 0,
    progressMessage: '等待生成',
    generatedVideoUrl: '',
    history: [],
    previewVideoUrl: '',
    userId: 1,  // 示例用户ID，可以通过登录系统获取
    images: [
      { value: 'default_image', label: '默认形象' },
      { value: 'image1', label: '形象1' },
      { value: 'image2', label: '形象2' }
    ],
    backgrounds: [
      { value: 'default_background', label: '默认背景' },
      { value: 'background1', label: '背景1' },
      { value: 'background2', label: '背景2' }
    ]
  },
  methods: {
    uploadAudio(event) {
      const file = event.target.files[0];
      const formData = new FormData();
      formData.append('file', file);
      axios.post('/path-to-your-upload-api', formData)
        .then(response => {
          this.inputAudioUrl = response.data.url;
        });
    },
    submitRequest() {
      const requestData = {
        user_id: this.userId,
        input_text: this.inputText,
        input_audio_url: this.inputAudioUrl,
        image: this.virtualImage,
        background: this.background
      };
      axios.post('/submit_request', requestData)
        .then(response => {
          this.requestId = response.data.request_id;
          this.checkStatus();
        });
    },
    checkStatus() {
      const intervalId = setInterval(() => {
        axios.get(`/status/${this.requestId}`)
          .then(response => {
            const status = response.data.status;
            if (status === 'pending') {
              this.progress = 25;
              this.progressMessage = '等待处理';
            } else if (status === 'processing') {
              this.progress = 50;
              this.progressMessage = '处理中';
            } else if (status === 'completed') {
              this.progress = 100;
              this.progressMessage = '已完成';
              this.fetchGeneratedVideo();
              clearInterval(intervalId);  // 停止轮询
            } else if (status === 'error') {
              this.progress = 0;
              this.progressMessage = '处理出错';
              clearInterval(intervalId);  // 停止轮询
            } else {
              this.progress = 0;
              this.progressMessage = '未知状态';
              clearInterval(intervalId);  // 停止轮询
            }
          });
      }, 5000);  // 每5秒查询一次状态
    },
    fetchGeneratedVideo() {
      axios.get(`/generated_video_url/${this.requestId}`)
        .then(response => {
          this.generatedVideoUrl = response.data.video_url;
        });
    },
    fetchHistory() {
      axios.get(`/history/${this.userId}`)
        .then(response => {
          this.history = response.data;
        });
    },
    preview(videoUrl) {
      this.previewVideoUrl = videoUrl;
    }
  },
  created() {
        this.fetchHistory();
  }
});
