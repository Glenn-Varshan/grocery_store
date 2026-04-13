<template>
  <div>
  <div class = "container" style="margin-top: 5px"  v-if="is_login">
    <form>
      <input style="margin-top: 5px;margin-left: 5px;" type="text" class="form" id="cat-name" placeholder="enter category name" v-model="searched.category">
      <input style="margin-top: 5px;margin-left: 5px;" type="text" class="form" id="item-name" placeholder="enter item name" v-model="searched.item">
      <input style="margin-top: 5px;margin-left: 5px;" type="number" class="form" id="item-price" placeholder="enter price" v-model="searched.price">
      <input style="margin-top: 5px;margin-left: 5px;" type="date" class="form" id="item-manufactured-date" placeholder="enter manufactured date" v-model="searched.manufactured_date">
      <button class=" btn-success" style="margin-top: 5px;margin-left: 10px;" @click.prevent="search()">SEARCH</button>
    </form>
    <router-link class="btn btn-primary" style="margin-top: 5px" to="/manager" v-if="role === 'User,StoreManager'|| role ==='Admin'">MANAGER DASHBOARD</router-link>
    <button class="btn btn-primary" style="margin-top: 5px" @click="apply()" v-if="role==='User'">Apply to be store manager</button>

    <div v-for="cat in category" :key="cat.id" >
      <div v-if="cat.is_approved" class="container-md p-4 my-5 bg-body border" style="border-radius: 1rem ;padding: 20px;">
      <h3>{{ cat.name }}</h3>
      <div v-for="item in items" :key="item.id" >
        <form>
          <div v-if="item.category_id===cat.id" class="container-md p-4 my-5 bg-light border"  style=" border-radius: 1rem ;padding: 10px;" >
            <h3>ITEM:{{ item.name }}</h3>
            <h3>PRICE:{{ item.rate}}</h3>
            <div v-if="item.stock === item.sold">
              <button class="btn btn-danger disabled" style="margin-top: 5px">NO STOCK</button>
            </div>
            <div v-else>
              <router-link :to="{name: 'product',params: {id: item.id}}" class="btn btn-success my-2">BUY</router-link>
            </div>
            
          </div>
        </form>
      </div>
    </div>
    </div>
  </div>
  <div class = "container" v-else>
    <main role="main" class="container">
      <h1 class="mt-5">YOU ARE NOT LOGGED IN</h1><p class="lead">Please login to access the store</p>
      
    </main>
  </div>
</div>
  
</template>

<script>
export default {
  data(){
    return{
      searched:{
        category:null,
        item:null,
        price:null,
        manufactured_date:null
      },
      items:[],
      category:[],
      role: localStorage.getItem('role'),
      is_login: localStorage.getItem('auth-token')
      
    }
  },
  methods:{
    async search(){
      this.searchcategory(),
      this.searchitem()
    },
    async searchcategory(){
          const res = await fetch("http://127.0.0.1:5000/api/search/category",{
            method: 'POST',
            headers:{
              "Content-type":'application/json',
              "Authentication-Token": localStorage.getItem('auth-token'),
            },
            body:JSON.stringify({"category" : this.searched['category']}),
          })
          if(res.ok){
            const data = await res.json()
            this.category =data
            console.log(data)
          }
          else{
            console.log("WRONG")
          }
        },
      async searchitem(){
          const res = await fetch("http://127.0.0.1:5000/api/search/item",{
            method: 'POST',
            headers:{
              "Content-type":'application/json',
              "Authentication-Token": localStorage.getItem('auth-token'),
            },
            body:JSON.stringify({"item" : this.searched.item, "price": this.searched.price, "manufactured_date": this.searched.manufactured_date}),
          })
          if(res.ok){
            const data = await res.json()
            this.items = data
            //this.category.push(...data)
            console.log(data)
          }
          else{
            console.log("WRONG")
          }
        },
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