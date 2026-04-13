<template>
  <div>
  <div class = "container" style="margin-top: 5px"  v-if="role === 'User,StoreManager'|| role ==='Admin'">
    <button class="btn btn-primary" style="margin-top: 20px" @click="download1()">DOWNLOAD INFO</button>
    <router-link class="btn btn-primary" to="/catadd" style="margin-top: 20px;margin-left: 5px;">ADD CATEGORY</router-link>
    <div v-for="cat in category" :key="cat.id" class="container-md p-4 my-5 bg-body border" style="border-radius: 1rem ;padding: 20px;">
      <h3>{{ cat.name }}</h3>
      <div v-for="item in items" :key="item.id" >
          <div v-if="item.category_id===cat.id" class="container-md p-4 my-5 bg-light border"  style=" border-radius: 1rem ;padding: 10px;" >
            <h3 >{{ item.name }}</h3>
            <router-link :to="{name: 'itemupdate',params: {id: item.id}}" class="btn btn-warning my-2" >Edit item</router-link>
            <button class="btn btn-danger my-2" style="margin-left: 5px;" @click="deleteItem(item.id)">Delete item</button>
          </div>
          
      </div>
      <router-link :to="{name: 'itemtask',params: {id: cat.id}}" class="btn btn-success my-2" >Add item</router-link>
    </div>
  </div>
  <div class = "container" v-else>
    <main role="main" class="container">
      <h1 class="mt-5">YOU DO NOT HAVE THE ROLES TO ACCESS THIS PAGE</h1><p class="lead">Please redirect to home page</p>
      
    </main>
  </div>
</div>
</template>

<script>
export default {
  data(){
    return{
      itemInput:{ 
          name:null,
          rate:null,
          quantity:null,
          manudate:null,
          expirydate: null,
        },
      items:[],
      category:[],
      role: localStorage.getItem('role'),
      is_login: localStorage.getItem('auth-token')
    }
  },
  methods:{
    async download1(){
      fetch('http://127.0.0.1:5000/api/infodownload',{
        method:"GET",
        headers:{
          "Content-type":"application/json",
          "Authentication-Token": localStorage.getItem('auth-token'),
        }
      }).then(resp => resp.json())
      .then(data => {
        const taskId = data['task_id']
        console.log(taskId)
        const intv =  setInterval(async () =>{
          const csv_res = await fetch('http://127.0.0.1:5000/get-csv/'+taskId)
          if(csv_res.ok){
            clearInterval(intv)
            window.location.href = 'http://127.0.0.1:5000/get-csv/'+taskId
          }
        },1000)
      })
      .catch(error => {
        console.log(error)
      })
    },
    deleteItem(itemid){
      fetch('http://127.0.0.1:5000/api/item/'+itemid,{
        method:"Delete",
        headers:{
          "Content-type":"application/json",
          "Authentication-Token": localStorage.getItem('auth-token'),
        }
      }).then(resp => resp.json())
      .catch(error => {
        console.log(error)
      })
    },
    getItems(){
      fetch('http://127.0.0.1:5000/api/item',{
        method:"GET",
        headers:{
          "Content-type":"application/json",
          "Authentication-Token": localStorage.getItem('auth-token'),
        }
      }).then(resp => resp.json())
      .then(data => {
        this.items.push(...data)
      })
      .catch(error => {
        console.log(error)
      })
    },
  getCategory(){
      fetch('http://127.0.0.1:5000/api/category',{
        method:"GET",
        headers:{
          "Content-type":"application/json",
          "Authentication-Token": localStorage.getItem('auth-token'),
        }
      }).then(resp => resp.json())
      .then(data => {
        this.category.push(...data)
      })
      .catch(error => {
        console.log(error)
      })
    },
  },
  created(){
    this.getItems(),
    this.getCategory()
  }
}
</script>

<style>

</style>