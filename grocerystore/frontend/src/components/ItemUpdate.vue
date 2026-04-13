<template>
  <div>
    <div class="d-flex justify-content-center mb-2" style="margin-top: 20vh;border-radius: 1rem;">
      <form>
        <h1>UPDATE ITEM</h1>
    <div>
        <label>NAME:</label>
        <input style="margin-top: 10px;margin-bottom: 10px;" type="text" class="form-control" id="item-name" placeholder="enter item name" v-model="itemUpdate.name">
    </div>
    <div>
        <label>RATE:</label>
        <input style="margin-top: 10px;margin-bottom: 10px;" type="text" class="form-control" id="item-rate" placeholder="enter rate" v-model="itemUpdate.rate">
    </div>
    <div>
        <label>STOCK:</label>
        <input style="margin-top: 10px;margin-bottom: 10px;" type="text" class="form-control" id="item-stock" placeholder="enter stock" v-model="itemUpdate.stock">
    </div>
    <div>
        <label>MANUFACTURED DATE:</label>
        <input style="margin-top: 10px;margin-bottom: 10px;" type="text" class="form-control" id="item-manudate" onfocus="(this.type='date')" v-model="itemUpdate.manudate">
    </div>
    <div>
        <label>EXPIRY DATE:</label>
        <input style="margin-top: 10px;margin-bottom: 10px;" type="text" class="form-control" id="item-expirydate" onfocus="(this.type='date')" min="{{this.item.expiry_date}}"  v-model="itemUpdate.expiry_date">
    </div>
        <button class="btn btn-success my-2" @click.prevent="updateItem()">Update item</button>
      </form>
    </div>
    </div>
</template>

<script>
export default {
    data(){
    return{
      itemUpdate:{ 
          name:null,
          rate:null,
          stock:null,
          manudate:null,
          expiry_date: null,
        },
      item:[],
      category:[],
      role: localStorage.getItem('role'),
      is_login: localStorage.getItem('auth-token')
    }
  },
    props:{
        id:{
            type:[Number,String],
            required:true
        },
    },
    methods:{
    updateItem(){
        fetch('http://127.0.0.1:5000/api/item/'+this.id,{
        method:"PUT",
        headers:{
            "Content-type":"application/json",
            "Authentication-Token": localStorage.getItem('auth-token'),
            },
            body:JSON.stringify({name:this.itemUpdate.name,rate:this.itemUpdate.rate, stock:this.itemUpdate.stock,manufactured_date : this.itemUpdate.manudate, expiry_date:this.itemUpdate.expiry_date})
      })
      .then(resp => resp.json())
      .then(() => {
        //this.$router.push({path:'/manager'})
      })
      .catch(error => {
        console.log(error)
      })

      },
      
    async gitem(){
          const res = await fetch('http://127.0.0.1:5000/api/item/'+this.id,{
            method: 'GET',
            headers:{
              "Content-type":'application/json',
              "Authentication-Token": localStorage.getItem('auth-token'),
            },
          })
          if(res.ok){
            const data = await res.json()
            this.item = data
            this.itemUpdate.name = this.item.name
            this.itemUpdate.rate = this.item.rate
            this.itemUpdate.stock = this.item.stock
            this.itemUpdate.manudate= this.item.manufactured_date
            this.itemUpdate.expiry_date = this.item.expiry_date
          }
          else{
            console.log("WRONG")
          }
        },
},
created(){
    this.gitem()

},
}
</script>

<style>

</style>