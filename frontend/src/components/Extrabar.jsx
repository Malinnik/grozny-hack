const ExtraBar = ({showSidebar = false, toggleSidebar}) => {
    return (
        <div className={`fixed top-0 right-0 h-full sm:w-96 w-screen bg-gray-100 border-r-[1px] border-gray-200 text-white transform ${showSidebar ? 'translate-x-0' : 'translate-x-full'} transition-transform duration-300` }>
            <div className="p-4">
              <h2 className="text-xl font-bold mb-4"></h2>
              <button onClick={toggleSidebar} className="absolute top-4 right-4 inline-block bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">Закрыть</button>
              <div className= "mt-4 text-black overflow-y-auto">
              

              </div>
            </div>
        </div>
    )
}

export default ExtraBar;