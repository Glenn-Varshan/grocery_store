<template>
  <div>
    <div class="d-flex justify-content-center mb-2" style="margin-top: 20vh;border-radius: 1rem;">
      <form>
        <h1>ADD CATEGORY</h1>
    <div>
        <label>NAME:</label>
        <input style="margin-top: 10px;margin-bottom: 10px;" type="text" class="form-control" id="item-name" placeholder="enter cat name" v-model="catInput.name">
    </div>
        <button class="btn btn-success my-2" @click="catadd()">ADD CATEGORY</button>
      </form>
    </div>
    </div>
</template>

<script>
export default {
    data(){
    return{
      catInput:{ 
          name:null,
        },
    }
  },
  methods:{
  catadd(){
    fetch('http://127.0.0.1:5000/api/category',{
        method:"POST",
        headers:{
            "Content-type":"application/json",
            "Authentication-Token": localStorage.getItem('auth-token'),
            },
            body:JSON.stringify({name:this.catInput.name})
      })
      .then(resp => resp.json())
      .then(() => {
        //this.$router.push({path:'/manager'})
      })
      .catch(error => {
        console.log(error)
      })

  },
}
}
</script>

<style>

</style>