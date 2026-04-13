<template>
  <div class="container-md p-4 my-5 bg-light border">
      <p>TOTAL PRICE:{{ total }}</p>
    <div v-for="item in usercart" :key="item.id">
      <div class="container-md p-4 my-5 bg-light border"  style=" border-radius: 1rem ;padding: 10px;" >
        <p>Name: {{item.name}}</p>
        <p>Price: {{item.rate}}</p>
        <p>Quantity: {{item.quantity}}</p>
        <p>Amount: {{item.amount}}</p>
      </div>
    </div>
  </div>
  </template>
  
  <script>
  export default {
    
    data(){
      return{
        usercart:[],
        amount:0,
      }
    },
    methods:{
      getCart(){
      fetch('http://127.0.0.1:5000/api/carttask',{
        method:"GET",
        headers:{
          "Content-type":"application/json",
          "Authentication-Token": localStorage.getItem('auth-token'),
        }
      }).then(resp => resp.json())
      .then(data => {
        this.usercart.push(...data)
        console.log(data)
      })
      .catch(error => {
        console.log(error)
      })
    },
    },
    computed:{
      total(){
        return this.usercart.reduce((total,curr) => (total = total + curr.amount),0)
    },
  },
    created(){
    this.getCart()
  }
  }
  </script>
  
  <style>
  
  </style>