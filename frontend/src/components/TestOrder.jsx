import React from 'react';
import axios from 'axios';

const TestOrder = () => {
  const testOrder = async () => {
    const orderData = {
      customer_name: "Test Customer",
      customer_email: "test@example.com", 
      customer_phone: "9876543210",
      shipping_address: "123 Test Street",
      notes: "",
      items: [
        {
          product: 1,
          quantity: 2,
          package_size: "1",
          unit_type: "Ltr",
          price: 150.00
        }
      ]
    };

    try {
      const response = await axios.post('http://localhost:8000/api/orders/', orderData);
      console.log('Order created:', response.data);
      alert('Test order created successfully!');
    } catch (error) {
      console.error('Error:', error.response?.data || error.message);
      alert('Error creating order: ' + JSON.stringify(error.response?.data || error.message));
    }
  };

  return (
    <div className="p-4">
      <button 
        onClick={testOrder}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        Test Order Creation
      </button>
    </div>
  );
};

export default TestOrder;