function Footer() {
  return (
    <footer className="bg-indigo-600 text-white mt-auto">
      <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 text-center">
        <p className="text-sm">
          &copy; {new Date().getFullYear()} QuizApp. All rights reserved. | Built with React & Flask.
        </p>
      </div>
    </footer>
  );
}
export default Footer;