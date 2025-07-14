import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white mt-auto">
      <div className="container mx-auto px-4 py-8 md:py-12">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 md:gap-8">
          <div className="sm:col-span-2 lg:col-span-1">
            <h3 className="text-lg md:text-xl font-bold mb-3 md:mb-4 font-gujarati">બજરંગ મિની ઓઇલ મિલ</h3>
            <p className="text-gray-300 mb-3 md:mb-4 text-sm md:text-base">
              Premium Quality Cold-Pressed Edible Oil Manufacturer
            </p>
          </div>
          
          <div>
            <h4 className="text-base md:text-lg font-semibold mb-3 md:mb-4">Quick Links</h4>
            <ul className="space-y-1 md:space-y-2 text-sm md:text-base">
              <li><Link to="/" className="text-gray-300 hover:text-white transition-colors">Home</Link></li>
              <li><Link to="/products" className="text-gray-300 hover:text-white transition-colors">Products</Link></li>
              <li><Link to="/about" className="text-gray-300 hover:text-white transition-colors">About Us</Link></li>
              <li><Link to="/gallery" className="text-gray-300 hover:text-white transition-colors">Gallery</Link></li>
              <li><Link to="/contact" className="text-gray-300 hover:text-white transition-colors">Contact</Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-base md:text-lg font-semibold mb-3 md:mb-4">Contact Info</h4>
            <div className="space-y-1 md:space-y-2 text-gray-300 text-sm md:text-base">
              <p>Kamleshbhai Ramani: <a href="tel:9979943944" className="hover:text-white">9979943944</a></p>
              <p>Hasmukhbhai Ramani: <a href="tel:9376319000" className="hover:text-white">9376319000</a></p>
              <p>Meet Ramani: <a href="tel:9979943944" className="hover:text-white">9979843944</a></p>
            </div>
          </div>
          
          <div>
            <h4 className="text-base md:text-lg font-semibold mb-3 md:mb-4">Location</h4>
            <p className="text-gray-300 text-xs md:text-sm mb-3 md:mb-4 leading-relaxed">
              Near B-59 Matruchhaya Raw House,<br />
              Ganga Jamna Society Rd,<br />
              Surat, Gujarat 395006
            </p>
            <p className="text-gray-300 text-xs md:text-sm">
              <strong>Hours:</strong> Mon-Sun 8AM-8PM
            </p>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-6 md:mt-8 pt-6 md:pt-8 text-center">
          <p className="text-gray-300 text-xs md:text-sm">
            © 2024 Bajrang Mini Oil Mill. All rights reserved.<br className="sm:hidden" />
            <span className="sm:ml-2">Pure infront manufacturing</span>
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;