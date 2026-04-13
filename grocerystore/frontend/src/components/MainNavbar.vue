<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class = "container">
      <router-link class="navbar-brand" to="/">GROCERY STORE</router-link>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item mx-2" v-if="role ==='Admin'">
          <router-link class="btn btn-primary" to="/admin">ADMIN</router-link>
        </li>
        <li class="nav-item mx-2"  v-if="!is_login">
          <router-link class="btn btn-primary" to="/login">LOGIN</router-link>
        </li>
        <li class="nav-item">
          <router-link class="btn btn-primary" to="/signup">SIGNUP</router-link>
        </li>
        <li class="nav-item mx-2" v-if="is_login">
          <router-link class="btn btn-success" to="/cart">CART</router-link>
        </li>
        <li class="nav-item mx-2" v-if="is_login">
          <a class="btn btn-danger" @click.prevent="logout">LOGOUT</a>
        </li>
      </ul>
    </div>
    </div>
</nav>
</template>

<script>
export default {
  data(){
      return{
        role: localStorage.getItem('role'),
        is_login: localStorage.getItem('auth-token')
      }
    },
  methods:{
     logout(){
          localStorage.clear()
          this.$router.push({name: 'login'})
        }
    },
    
}

</script>

<style>

</style>