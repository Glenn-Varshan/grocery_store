<template>
  <div>
    <div class = "container" style="margin-top: 5px"  v-if="role==='Admin'">
      
      <div class="container-md p-4 my-5 bg-light border" style=" border-radius: 1rem ;padding: 10px;">
        <router-link class="btn btn-primary" to="/catadd" style="margin-top: 5px;margin-bottom: 20px;">ADD CATEGORY</router-link>
        <h3 >CATEGORY REQUESTS</h3>
          <div v-for="cat in category" :key="cat.id" class="container-md p-4 my-5 bg-body border" style="border-radius: 1rem ;padding: 20px;">
            <h3>{{ cat.name }}</h3>
              <div v-for="item in items" :key="item.id" >
                  <div v-if="item.category_id===cat.id" class="container-md p-4 my-5 bg-light border"  style=" border-radius: 1rem ;padding: 10px;" >
                    <h3 >{{ item.name }}</h3>
                    <button class="btn btn-warning my-2" @click="editItem()">Edit item</button>
                    <button class="btn btn-danger my-2" @click="deleteItem(item.id)">Delete item</button>
                  </div>
              </div>
            <div v-if="!cat.is_approved">
              <button class="btn btn-success my-2" @click="approve(cat.id)">Approve</button>
            </div>
            <button class="btn btn-danger my-2" @click="deleteCat(cat.id)">Delete category</button>
          </div>
          </div>
          <div class="container-md p-4 my-5 bg-light border" style=" border-radius: 1rem ;padding: 10px;">
            <h3>STORE MANAGER REQUESTS</h3>
            <div v-for="req in requests" :key="req.id" >
              <div  style=" border-radius: 1rem ;padding: 10px;">
              <div v-if="!req.is_approved">
                <p>{{ req.email }}</p>
                <button class="btn btn-success my-2" @click="approveSM(req.user_id)">Approve store manager</button>
              </div>
              </div>
            </div>
          </div>
      </div>
    <div class = "container" v-else>
      <main role="main" class="container">
        <h1 class="mt-5">YOU ARE NOT AN ADMIN</h1><p class="lead">Please go back</p>
      </main>
    </div>
  </div>
</template>
  
  <script>
  export default {
  data(){
      return{
        items:[],
        category:[],
        requests:[],
        role: localStorage.getItem('role'),
        is_login: localStorage.getItem('auth-token')
      }
    },
    methods:{
      deleteCat(catid){
      fetch('http://127.0.0.1:5000/api/category/'+catid,{
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
      getRequests(){
      fetch('http://127.0.0.1:5000/api/adminreq',{
        method:"GET",
        headers:{
          "Content-type":"application/json",
          "Authentication-Token": localStorage.getItem('auth-token'),
        }
      }).then(resp => resp.json())
      .then(data => {
        this.requests.push(...data)
        console.log(this.requests)
      })
      .catch(error => {
        console.log(error)
      })
    },
      approve(itemid){
      fetch('http://127.0.0.1:5000/category/'+itemid+'/approve',{
        method:"Get",
        headers:{
          "Content-type":"application/json",
          "Authentication-Token": localStorage.getItem('auth-token'),
        }
      }).then(resp => resp.json())
      .catch(error => {
        console.log(error)
      })
    },
    approveSM(userid){
      fetch('http://127.0.0.1:5000/user/'+userid+'/approve',{
        method:"Get",
        headers:{
          "Content-type":"application/json",
          "Authentication-Token": localStorage.getItem('auth-token'),
        }
      }).then(resp => resp.json()).then(data => {
        console.log(data)
      })
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
    this.getRequests()
    this.getItems(),
    this.getCategory()
  }
}
  </script>
  
  <style>
  
  </style>