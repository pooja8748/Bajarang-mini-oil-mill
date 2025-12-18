import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { cartAPI } from '../services/api';

const CartContext = createContext();

const cartReducer = (state, action) => {
  switch (action.type) {
    case 'SET_CART':
      return { ...state, items: action.payload, loading: false };
    case 'ADD_ITEM':
      return { ...state, items: [...state.items, action.payload] };
    case 'UPDATE_ITEM':
      return {
        ...state,
        items: state.items.map(item =>
          item.id === action.payload.id ? action.payload : item
        )
      };
    case 'REMOVE_ITEM':
      return {
        ...state,
        items: state.items.filter(item => item.id !== action.payload)
      };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    default:
      return state;
  }
};

export const CartProvider = ({ children }) => {
  const [state, dispatch] = useReducer(cartReducer, {
    items: [],
    loading: true
  });

  const fetchCart = async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      // Load from localStorage for development
      const savedCart = localStorage.getItem('cart');
      const cartItems = savedCart ? JSON.parse(savedCart) : [];
      dispatch({ type: 'SET_CART', payload: cartItems });
    } catch (error) {
      console.error('Error fetching cart:', error);
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const addToCart = async (item) => {
    try {
      // For development, use local storage instead of API
      const cartItem = {
        id: Date.now(),
        product: item.product || 1, // Default to product ID 1
        product_name: item.product_name || 'Product',
        product_image: item.product_image,
        quantity: item.quantity,
        package_size: item.package_size || '1',
        unit_type: item.unit_type || 'Ltr',
        price: item.price,
        total_price: item.price * item.quantity
      };
      dispatch({ type: 'ADD_ITEM', payload: cartItem });
      
      // Save to localStorage
      const updatedItems = [...state.items, cartItem];
      localStorage.setItem('cart', JSON.stringify(updatedItems));
    } catch (error) {
      console.error('Error adding to cart:', error);
    }
  };

  const updateCartItem = async (id, data) => {
    try {
      const updatedItem = { ...state.items.find(item => item.id === id), ...data };
      updatedItem.total_price = updatedItem.price * updatedItem.quantity;
      dispatch({ type: 'UPDATE_ITEM', payload: updatedItem });
      
      const updatedItems = state.items.map(item => 
        item.id === id ? updatedItem : item
      );
      localStorage.setItem('cart', JSON.stringify(updatedItems));
    } catch (error) {
      console.error('Error updating cart item:', error);
    }
  };

  const removeFromCart = async (id) => {
    try {
      dispatch({ type: 'REMOVE_ITEM', payload: id });
      const updatedItems = state.items.filter(item => item.id !== id);
      localStorage.setItem('cart', JSON.stringify(updatedItems));
    } catch (error) {
      console.error('Error removing from cart:', error);
    }
  };

  const getTotalPrice = () => {
    return state.items.reduce((total, item) => total + item.total_price, 0);
  };

  const getTotalItems = () => {
    return state.items.reduce((total, item) => total + item.quantity, 0);
  };

  const clearCart = () => {
    dispatch({ type: 'SET_CART', payload: [] });
    localStorage.removeItem('cart');
  };

  useEffect(() => {
    fetchCart();
  }, []);

  return (
    <CartContext.Provider value={{
      ...state,
      addToCart,
      updateCartItem,
      removeFromCart,
      getTotalPrice,
      getTotalItems,
      clearCart,
      fetchCart
    }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within CartProvider');
  }
  return context;
};