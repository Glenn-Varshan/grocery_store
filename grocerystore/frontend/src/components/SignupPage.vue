<template>
  <div class="d-flex justify-content-center" style="margin-top: 20vh">
    <div class="card bg-light" style="border-radius: 1rem;">
      <div class="card-body p-5 text-center">
  <form @submit.prevent="signup">
    <h2 class="fw-bold mb-2 text-uppercase">SIGNUP</h2>
    <div class="mb-md-5 mt-md-4 pb-2">
    <input type="email" class="form-control" aria-describedby="emailHelp" placeholder="enter email" v-model="email">
  </div>
  <div class="mb-md-1 mt-md-4 pb-2">
    <input type="password" class="form-control" placeholder="enter password" v-model="password">
  </div>
  <button class="btn btn-primary my-2">SIGNUP</button>
</form>
</div>
</div>
</div>
</template>

<script>
export default {
    data(){
      return{
        email:null,
        password:null,
        error:null
      }
    },
    methods:{
      signup()
      {
          if(!this.email || !this.password){
            this.error = "Please add all fields"
          }else{
            fetch('http://127.0.0.1:5000/api/user',{
            method:"POST",
            headers:{
            "Content-type":"application/json"
            },
            body:JSON.stringify({email:this.email,password:this.password})
      })
      .then(resp => resp.json())
      .then(() => {
          this.$router.push({
          name: 'login'
        })
      })
      .catch(error => {
        console.log(error)
      })
        }
      }
    }
}
</script>

<style>

</style>