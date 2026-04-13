<template>
  <div class="d-flex justify-content-center" style="margin-top: 20vh">
    <div class="card bg-light" style="border-radius: 1rem;">
      <div class="card-body p-5 text-center">
    <form @submit.prevent="login">
      <h2 class="fw-bold mb-2 text-uppercase">LOGIN</h2>
  <div class="mb-md-5 mt-md-4 pb-2">
    <input type="email" class="form-control"  id= "user-email" aria-describedby="emailHelp" placeholder="enter email" v-model="cred.email">
  </div>
  <div class="mb-md-1 mt-md-4 pb-2">
    <input type="password" class="form-control" id="user-password" placeholder="enter password" v-model="cred.password">
  </div>
  <button class="btn btn-primary my-2 ">LOGIN</button>
</form>

</div>
</div>
</div>
</template>

<script>
export default {
  data(){
      return{
        cred:{ 
          email:null,
          password:null,
        },
        userRole:null
      }
    },
  methods:{
    apply(){
      fetch('http://127.0.0.1:5000/apply',{
        method:"GET",
        headers:{
          "Content-type":"application/json",
          "Authentication-Token": localStorage.getItem('auth-token'),
        }
      }).then(resp => resp.json())
      .catch(error => {
        console.log(error)
      })
    },
    async login(){
      if(!this.cred.email || !this.cred.password){
            this.error = "Please add all fields"
          }else{
          const res = await fetch("http://127.0.0.1:5000/user-login",{
            method: 'POST',
            headers:{
              "Content-type":'application/json',
            },
            body:JSON.stringify(this.cred),
          })
          if(res.ok){
            const data = await res.json()
            this.userRole = data.role
            localStorage.setItem('auth-token', data.token)
            localStorage.setItem('role', data.role)
            this.$router.push({path:'/'})
          }
          else{
            console.log("WRONG")
          }
          }
        }
      
    }
  }
</script>

<style>

</style>