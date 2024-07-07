const Pagination = ({page, max_page, prev_page, next_page}) => {

    if (page === 1) {
        return (
            <div className="lg:col-start-3 md:col-start-2 relative col-span-1 flex items-center">
                <button disabled='disabled' onClick={prev_page} className="w-full p-4 border text-base rounded-l-xl text-gray-600 bg-white ">
                    <svg width="9" fill="currentColor" height="8" viewBox="0 0 1792 1792" xmlns="http://www.w3.org/2000/svg">
                        <path d="M1427 301l-531 531 531 531q19 19 19 45t-19 45l-166 166q-19 19-45 19t-45-19l-742-742q-19-19-19-45t19-45l742-742q19-19 45-19t45 19l166 166q19 19 19 45t-19 45z">
                        </path>
                    </svg>
                </button>
                <button className="w-full px-4 py-2 border-t border-b text-base text-blue-500 bg-white hover:bg-gray-200">
                    {page}
                </button>
                <button className="w-full px-4 py-2 border text-base text-gray-600 bg-white hover:bg-gray-200">
                    {page+1}
                </button>
                <button className="w-full px-4 py-2 border-t border-b text-base text-gray-600 bg-white hover:bg-gray-200">
                    {page+2}
                </button>
                <button onClick={next_page} className="text-center w-full p-4 border-t border-b border-r text-base rounded-r-xl text-gray-600 bg-white hover:bg-gray-200">
                    <svg width="9" fill="currentColor" height="8" viewBox="0 0 1792 1792" xmlns="http://www.w3.org/2000/svg">
                        <path d="M1363 877l-742 742q-19 19-45 19t-45-19l-166-166q-19-19-19-45t19-45l531-531-531-531q-19-19-19-45t19-45l166-166q19-19 45-19t45 19l742 742q19 19 19 45t-19 45z">
                        </path>
                    </svg>
                </button>
            </div>
        )
    }

    if (page === max_page)  {
        return (
            <div className="lg:col-start-3 md:col-start-2 relative col-span-1 flex items-center">
                <button onClick={prev_page} className="w-full p-4 border text-base rounded-l-xl text-gray-600 bg-white hover:bg-gray-200">
                    <svg width="9" fill="currentColor" height="8" viewBox="0 0 1792 1792" xmlns="http://www.w3.org/2000/svg">
                        <path d="M1427 301l-531 531 531 531q19 19 19 45t-19 45l-166 166q-19 19-45 19t-45-19l-742-742q-19-19-19-45t19-45l742-742q19-19 45-19t45 19l166 166q19 19 19 45t-19 45z">
                        </path>
                    </svg>
                </button>
                <button className="w-full px-4 py-2 border text-base text-gray-600 bg-white hover:bg-gray-200">
                    {page-2}
                </button>
                <button className="w-full px-4 py-2 border text-base text-gray-600 bg-white hover:bg-gray-200">
                    {page-1}
                </button>
                <button className="w-full px-4 py-2 border-t border-b text-base text-blue-500 bg-white hover:bg-gray-200">
                    {page}
                </button>
                <button  onClick={next_page} disabled='disabled' className="text-center w-full p-4 border-t border-b border-r text-base rounded-r-xl text-gray-600 bg-white hover:bg-gray-200">
                    <svg width="9" fill="currentColor" height="8" viewBox="0 0 1792 1792" xmlns="http://www.w3.org/2000/svg">
                        <path d="M1363 877l-742 742q-19 19-45 19t-45-19l-166-166q-19-19-19-45t19-45l531-531-531-531q-19-19-19-45t19-45l166-166q19-19 45-19t45 19l742 742q19 19 19 45t-19 45z">
                        </path>
                    </svg>
                </button>
            </div>
        )
    }

    return (
        <div className="lg:col-start-3 md:col-start-2 relative col-span-1 flex items-center">
            <button onClick={prev_page} className="w-full p-4 border text-base rounded-l-xl text-gray-600 bg-white hover:bg-gray-200">
                <svg width="9" fill="currentColor" height="8" viewBox="0 0 1792 1792" xmlns="http://www.w3.org/2000/svg">
                    <path d="M1427 301l-531 531 531 531q19 19 19 45t-19 45l-166 166q-19 19-45 19t-45-19l-742-742q-19-19-19-45t19-45l742-742q19-19 45-19t45 19l166 166q19 19 19 45t-19 45z">
                    </path>
                </svg>
            </button>
            <button className="w-full px-4 py-2 border-t border-b text-base text-gray-600 bg-white hover:bg-gray-200">
                {page-1}
            </button>
            <button className="w-full px-4 py-2 border-t border-b text-base text-blue-500 bg-white hover:bg-gray-200">
                {page}
            </button>
            <button className="w-full px-4 py-2 border-t border-b text-base text-gray-600 bg-white hover:bg-gray-200">
                {page+1}
            </button>
            <button onClick={next_page} className="text-center w-full p-4 border-t border-b border-r text-base rounded-r-xl text-gray-600 bg-white hover:bg-gray-200">
                <svg width="9" fill="currentColor" height="8" viewBox="0 0 1792 1792" xmlns="http://www.w3.org/2000/svg">
                    <path d="M1363 877l-742 742q-19 19-45 19t-45-19l-166-166q-19-19-19-45t19-45l531-531-531-531q-19-19-19-45t19-45l166-166q19-19 45-19t45 19l742 742q19 19 19 45t-19 45z">
                    </path>
                </svg>
            </button>
        </div>
    )
}

export default Pagination
