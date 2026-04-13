<template>
    <div class="d-flex justify-content-center " style="margin-top: 10vh" >
        <form @submit="Buy">
            <div class="card bg-light text-center" style="border-radius: 1rem;padding: 100px;">
            <h1>PRODUCT </h1>
            <p>ITEM: {{ item['name'] }}</p>
            <p>AVAILABILTY: {{ item['stock'] - item['sold'] }}</p>
            <p>RATE: {{ item['rate'] }}</p>
            <p>MANUFACTURED DATE: {{ item['manufactured_date'] }}</p>
            <p>EXPIRY DATE: {{ item['expiry_date'] }}</p>
            <div class="mb-md-1 mt-md-4 pb-2" v-if="!(item['sold']===item['stock'])">
                <input type="number" class="form-control" id="amount" placeholder="enter amount" v-model="buying">
            </div>
        <button v-if="item['sold']===item['stock']" class="btn btn-danger disabled my-2">NO STOCK</button>
        <button v-else class="btn btn-primary my-2">Add to cart</button>
    </div>
        </form>
    </div>
</template>

<script>
export default {
    data(){
        return {
                item:{},
                buying:null,
        };
    },
    props:{
        id:{
            type:[Number,String],
            required:true
        },
    },
    methods:{
    getItemData(){
      fetch('http://127.0.0.1:5000/api/item/'+this.id,{
        method:"GET",
        headers:{
          "Content-type":"application/json",
          "Authentication-Token": localStorage.getItem('auth-token'),
        }
      }).then(resp => resp.json())
      .then(data => {
        this.item = data
      })
      .catch(error => {
        console.log(error)
      })
    },
     Buy(){
          const res = fetch("http://127.0.0.1:5000/api/cart",{
            method: 'POST',
            headers:{
              "Content-type":'application/json',
              "Authentication-Token": localStorage.getItem('auth-token'),
            },
            body:JSON.stringify({name: this.item['name'], rate: this.item["rate"], quantity: this.buying,item_id: this.item["id"]}),
          })
          if(res.ok){
            const data = res.json()
            console.log(data)
            this.$router.push({path:'/'})
          }
          }
      
    },
    created(){
    this.getItemData()
  }
}
</script>

<style>

</style>