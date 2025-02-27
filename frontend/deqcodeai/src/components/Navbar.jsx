
const Navbar = ({ username }) => {
  return (
    <nav className="bg-gray-900 text-white p-4 flex items-center">
      <h1 className="text-xl font-bold ml-auto">Quantum Circuits</h1>
      <span className="text-orange-400 ml-auto">{username}</span>
    </nav>
  );
};

export default Navbar;
