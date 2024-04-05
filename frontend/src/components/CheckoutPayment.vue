<script setup>
import { loadScript } from '@paypal/paypal-js'
import { onBeforeMount, ref } from 'vue'

const CLIENT_ID = import.meta.env.VITE_PAYPAL_API_CLIENT

const { cartTotal } = defineProps({
  cartTotal: {
    type: Number,
    default: 10,
  }
})
const paid  = ref(false)

onBeforeMount(function() {
    loadScript({ 'client-id': CLIENT_ID }).then((paypal) => {
      paypal
        .Buttons({
          fundingSource: paypal.FUNDING.PAYPAL,
          createOrder: createOrder,
          onApprove: onApprove,
        })
        .render('#paypal-button-container')
    })
  })

   function createOrder(data, actions) {
      console.log('Creating order...')
      return actions.order.create({
        purchase_units: [
          {
            amount: {
              value: 10,
            },
          },
        ],
      })
    }

function onApprove(data, actions) {
  console.log('Order approved...')
  return actions.order.capture().then(() => {
    paid.value = true
    console.log('Order complete!')
  })
}
</script>

<template>
  <div v-if="!paid" id="paypal-button-container"></div>
  <div v-else id="confirmation">Order complete!</div>
</template>

<style>
#paypal-button-container {
  width: 100%;
  margin: 30px 0;
}

#confirmation {
  color: green;
  margin-top: 1em;
  font-size: 2em;
}
</style>