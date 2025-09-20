import Image from 'next/image'
import React from 'react'

function Header() {
  return (
    <div className='header'>
      <div className='header-logo'>
        <a href="http://www.ipu.ac.in/" target="_blank" rel="noopener noreferrer">
          <Image 
            src="/ipu-logo.png" 
            alt="IPU Logo" 
            width={300} 
            height={300} 
            className="cursor-pointer"
          />
        </a>
      </div>
    </div>
  )
}

export default Header