<template lang="html">
  <div class="photograph_page">

    <h3 class="pageTitle">Sweet Toothy Smile <Icon type="md-contacts" size="25"/></h3>

    <div>
      <div class="video_box">
        <div class="border" v-if="!isShowImg">
          <span class="top_left"></span>
          <span class="top_right"></span>
          <span class="bottom_left"></span>
          <span class="bottom_right"></span>
        </div>
        <video ref="video" v-if="!isShowImg"></video>
        <img ref="img" class="img" v-show="isShowImg">
      </div>
      <canvas class="canvas" v-show="false" ref="canvas"></canvas>
    </div>
    <br/>
    <div class="button_group">
      <i-button v-show="isShowImg"  @click.native="resetPhoto">Retake</i-button>
      <i-button v-show="isShowImg" @click.native="surePhoto">Detect</i-button>
      <i-button @click.native="photo" v-show="!isShowImg">Take</i-button>
    </div>

  </div>
</template>

<script>
export default {
  name: 'Camera',
  data () {
    return {
      video: null,
      isShowImg: false,
      dataURL: null,
      track: null
    }
  },
  mounted () {
    this.initPhoto()
  },
  methods: {
    initPhoto () {
      let vm = this
      // 浏览器兼容
      let mediaDevices = navigator.mediaDevices.getUserMedia({audio: false, video: {width: 700, height: 500}})

      mediaDevices
        .then(mediaStream => {
          let video = vm.$refs.video
          video.src = window.URL.createObjectURL(mediaStream)
          video.onloadedmetadata = (e) => {
            video.play()
          }
          vm.video = video
          vm.track = mediaStream.getTracks()[0]
        })
        .catch(err => {
          console.log('err.message' + err.name)
        })
    },
    photo () {
      let dataURL = null
      let img = this.$refs.img
      let canvas = this.$refs.canvas
      let context = canvas.getContext('2d')
      let width = 700
      let height = 500
      canvas.width = width
      canvas.height = height
      img.height = height
      context.drawImage(this.video, 0, 0, width, height)
      dataURL = canvas.toDataURL('image/png')
      img.src = dataURL
      this.dataURL = dataURL
      this.isShowImg = true
    },
    resetPhoto () {
      this.dataURL = null
      this.video = null
      this.track = null
      this.isShowImg = false
      this.initPhoto()
    },
    surePhoto () {
      console.log(this.dataURL)
      // this.downloadFile('ship.png', this.dataURL)
      let postData = this.$qs.stringify({
        photo: this.dataURL.substring(22)
      })

      // test
      this.$axios.post('http://localhost:5000/camera', {
        photo: this.dataURL.substring(22)
      }).then(
        resp => this.$refs.img.src = resp.data.url,
        err => console.log(err)
      )
      // this.$axios({
      //   method: 'post',
      //   url: 'http://localhost:5000/camera',
      //   data: postData
      // }).then(function (response) {
      //   this.$refs.img.src = response.url
      //   this.$Message.success('Wait for detect...')
      //   console.log(response)
      // }).catch(function (error) {
      //   console.log(error)
      // })
    },
    stopPhoto () {
      this.track.stop()
    },
    base64Img2Blob (code) {
      var parts = code.split(';base64,')
      var contentType = parts[0].split(':')[1]
      var raw = window.atob(parts[1])
      var rawLength = raw.length
      var uInt8Array = new Uint8Array(rawLength)

      for (var i = 0; i < rawLength; ++i) {
        uInt8Array[i] = raw.charCodeAt(i)
      }

      return new Blob([uInt8Array], {type: contentType})
    },
    downloadFile (fileName, content) {
      var aLink = document.createElement('a')
      var blob = this.base64Img2Blob(content)
      var evt = document.createEvent('HTMLEvents')
      evt.initEvent('click', false, false)
      aLink.download = fileName
      aLink.href = URL.createObjectURL(blob)
      aLink.dispatchEvent(evt)
    }
  },
  destroyed () {
    let vm = this
    vm.stopPhoto()
  }
}
</script>

<style scoped>
  .photograph_page {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
  .button_group {
    margin-top:20px;
  }
  .video_box {
    /*width: 400px;*/
    /*height:500px;*/
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 1px 3px 10px #000;
    border: 10px solid #fff;
    background: #fff;
    border-radius: 2px;
    box-sizing: content-box;
  .video {
    z-index: 999;
    margin: 0;
  }
  .img {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 9999;
    display: block;
    background: red;
  }
  .border {
    width: 100%;
    height: 100%;
    position: absolute;
    top:0;
    bottom:0;
    left:0;
    right: 0;
  span {
    position: absolute;
    z-index: 99999;
    transform: translate3d(0, 0, 0);
    animation: flashing 1s linear 1s infinite alternate;
  }
  @border: 2px solid #000;
  @size: 20px;
  .top_left {
    border-top: @border;
    border-left: @border;
    top: @size;
    left: @size;
  }
  .top_right {
    border-top: @border;
    border-right: @border;
    top: @size;
    right: @size;
  }
  .bottom_left {
    border-bottom: @border;
    border-left: @border;
    bottom: @size;
    left: @size;
  }
  .bottom_right {
    border-right: @border;
    border-bottom: @border;
    right: @size;
    bottom: @size;
  }
  }
  }
  @keyframes flashing {
    0% {
      opacity: 1;
    }
    100% {
      opacity: 0;
    }
  }
</style>
