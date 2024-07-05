const ExtraBar = ({showSidebar = false, showResponseText = true, responseText, toggleSidebar}) => {
    return (
        <div className={`fixed top-0 right-0 h-full sm:w-96 w-screen bg-gray-100 border-r-[1px] border-gray-200 text-white transform ${showSidebar ? 'translate-x-0' : 'translate-x-full'} transition-transform duration-300` }>
            <div className="p-4">
              <h2 className="text-xl font-bold mb-4"></h2>
              <button onClick={toggleSidebar} className="absolute top-4 right-4 inline-block bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">Закрыть</button>
              <div className= "mt-4 text-black overflow-y-auto">
              
                <div> 
                  {/* <p className= "font-bold text-black text-xl text-center">Легенда</p>
                  <div> 
                    <h3 className= "text-black my-5">  
                      <p className= " text-blue-500 font-bold">СИНИЙ - прилегающие дефекты:</p>
                      {showResponseText && <span>Количество: {String(responseText.adj)}</span>}
                      <p className= "text-red-600 font-bold">КРАСНЫЙ - дефекты целостности:</p>
                      {showResponseText && <span>Количество: {String(responseText.int)}</span>}
                      <p className= " text-green-600 font-bold">ЗЕЛЕНЫЙ - дефекты геометрии:</p>
                      {showResponseText && <span>Количество: {String(responseText.geo)}</span>}
                      <p className= " text-violet-600 font-bold">ФИОЛЕТОВЫЙ - дефекты постобработки:</p> 
                      {showResponseText && <span>Количество: {String(responseText.pro)}</span>}
                      <p className= " text-yellow-500 font-bold">ЖЕЛТЫЙ - дефекты невыполнения:</p>                
                      {showResponseText && <span>Количество: {String(responseText.non)}</span>}
                    </h3> 
                  </div> */}
                </div>

              </div>
            </div>
        </div>
    )
}

export default ExtraBar;