<template>
  <div id="app">
    <MainNavbar :key="$route.fullPath"/>
    <router-view></router-view>
  </div>
</template>

<script>
import MainNavbar from './components/MainNavbar.vue'


export default {
  name: 'App',
  components: {
    MainNavbar
  },
}
</script>

<style>

</style>
