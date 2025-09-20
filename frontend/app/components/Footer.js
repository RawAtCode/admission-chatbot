import React from 'react';

function Footer() {
  return (
    <footer className="bg-[#041d54] text-white py-2 w-full">
      <div className="container mx-auto px-2 flex flex-col items-center text-center gap-2">
        <p className="text-sm italic">
          Disclaimer: This chatbot is unofficial and is not affiliated with GGSIPU.
        </p>

        <p className="text-sm">
          Developed by{' '}
          <a
            href="https://github.com/RawAtCode"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-gray-300"
          >
            RawAtCode
          </a>
        </p>
      </div>
    </footer>
  );
}

export default Footer;