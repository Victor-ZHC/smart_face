<template>
  <div id="app">
    <h1 style="float: left; margin-left: 40px; margin-top: 5px; display: inline;">
      <Icon type="ios-people-outline" size="40"/>
      Smart Face
    </h1>

    <div style="float: right; margin-right: 40px; display: inline;">
      <Menu mode="horizontal" :theme="light" active-name="1">
        <MenuItem name="1" to="/">
          <Icon type="ios-cloud-upload-outline" size="30"></Icon>
          Picture
        </MenuItem>
        <MenuItem name="2" to="/camera">
          <Icon type="ios-camera" size="30"></Icon>
          Camera
        </MenuItem>
      </Menu>
    </div>

    <Divider />
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 10px;
}
</style>
