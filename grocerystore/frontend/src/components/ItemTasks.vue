<template>
  <div>
    <div class="d-flex justify-content-center mb-2" style="margin-top: 20vh;border-radius: 1rem;">
      <form>
        <h1>ADD ITEM</h1>
    <div>
        <label>NAME:</label>
        <input style="margin-top: 10px;margin-bottom: 10px;" type="text" class="form-control" id="item-name" placeholder="enter item name" v-model="itemInput.name">
    </div>
    <div>
        <label>RATE:</label>
        <input style="margin-top: 10px;margin-bottom: 10px;" type="text" class="form-control" id="item-rate" placeholder="enter rate" v-model="itemInput.rate">
    </div>
    <div>
        <label>STOCK:</label>
        <input style="margin-top: 10px;margin-bottom: 10px;" type="text" class="form-control" id="item-stock" placeholder="enter stock" v-model="itemInput.stock">
    </div>
    <div>
        <label>MANUFACTURED DATE:</label>
        <input style="margin-top: 10px;margin-bottom: 10px;" type="date" class="form-control" id="item-manudate" placeholder="enter manufactured date" v-model="itemInput.manudate">
    </div>
    <div>
        <label>EXPIRY DATE:</label>
        <input style="margin-top: 10px;margin-bottom: 10px;" type="date" class="form-control" id="item-expirydate" placeholder="enter expiry date" v-model="itemInput.expirydate">
    </div>
        <button class="btn btn-success my-2" @click="addItem()">Add item</button>
      </form>
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
          stock:null,
          manudate:null,
          expirydate: null,
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
    addItem(){
        fetch('http://127.0.0.1:5000/api/item',{
        method:"POST",
        headers:{
            "Content-type":"application/json",
            "Authentication-Token": localStorage.getItem('auth-token'),
            },
            body:JSON.stringify({name:this.itemInput.name,rate:this.itemInput.rate, stock:this.itemInput.stock,manufactured_date : this.itemInput.manudate, expiry_date:this.itemInput.expirydate, category_id:this.id})
      })
      .then(resp => resp.json())
      .then(() => {
        this.$router.push({path:'/'})
      })
      .catch(error => {
        console.log(error)
      })

      }
}
}

</script>

<style>

</style>