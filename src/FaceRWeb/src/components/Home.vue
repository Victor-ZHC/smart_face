<template>
  <div>
    <div class="demo-upload-list" v-for="item in uploadList">
      <p>Gender: {{item.gender}}     Age: {{item.age}}</p>
      <template v-if="item.status === 'finished'">
        <img :src="item.url">
        <div class="demo-upload-list-cover">
          <Icon type="ios-eye-outline" @click.native="handleView(item.name)"></Icon>
          <Icon type="ios-trash-outline" @click.native="handleRemove(item)"></Icon>
        </div>
      </template>
      <template v-else>
        <Progress v-if="item.showProgress" :percent="item.percentage" hide-info></Progress>
      </template>
    </div>
    <Upload
      ref="upload"
      :on-success="handleSuccess"
      :format="['jpg','jpeg','png']"
      :max-size="2048"
      :on-format-error="handleFormatError"
      :on-exceeded-size="handleMaxSize"
      :before-upload="handleBeforeUpload"
      multiple
      type="drag"
      action="http://localhost:5000/upload"
      style="display: inline-block;width:255px;">
      <div style="width:255px;height:255px;line-height: 255px;">
        <Icon type="ios-camera" size="30"></Icon>
      </div>
    </Upload>
    <Modal title="View Image" v-model="visible">
      <img :src="'http://localhost:5000/images/' + imgName " v-if="visible" style="width: 100%">
    </Modal>
  </div>
</template>
<script>
export default {
  data () {
    return {
      imgName: '',
      visible: false,
      uploadList: []
    }
  },
  methods: {
    handleView (name) {
      this.imgName = name
      this.visible = true
    },
    handleRemove (file) {
      const fileList = this.uploadList
      this.uploadList.splice(fileList.indexOf(file), 1)
    },
    handleSuccess (res, file) {
      if (res.code === 0) {
        let ele = {'name': file.name, 'url': res.url, 'status': 'finished', 'gender': res.faces[0].gender, 'age': res.faces[0].age}
        this.uploadList.push(ele)
      } else {
        this.$Notice.warning({
          title: 'Upload Error',
          desc: 'Your file ' + file.name + 'upload was NOT successful.'
        })
      }
    },
    handleFormatError (file) {
      this.$Notice.warning({
        title: 'The file format is incorrect',
        desc: 'File format of ' + file.name + ' is incorrect, please select jpg or png.'
      })
    },
    handleMaxSize (file) {
      this.$Notice.warning({
        title: 'Exceeding file size limit',
        desc: 'File  ' + file.name + ' is too large, no more than 2M.'
      })
    },
    handleBeforeUpload () {
      const check = this.uploadList.length < 5
      if (!check) {
        this.$Notice.warning({
          title: 'Up to five pictures can be uploaded.'
        })
      }
      return check
    }
  }
}
</script>

<style>
  .demo-upload-list{
    display: inline-block;
    width: 300px;
    height: 330px;
    text-align: center;
    line-height: 60px;
    border: 1px solid transparent;
    border-radius: 4px;
    overflow: hidden;
    background: #fff;
    position: relative;
    box-shadow: 0 1px 1px rgba(0,0,0,.2);
    margin-right: 4px;
  }
  .demo-upload-list img{
    width: 100%;
    height: 100%;
  }
  .demo-upload-list-cover{
    display: none;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(0,0,0,.6);
  }
  .demo-upload-list:hover .demo-upload-list-cover{
    display: block;
  }
  .demo-upload-list-cover i{
    color: #fff;
    font-size: 20px;
    cursor: pointer;
    margin: 0 2px;
  }
</style>
