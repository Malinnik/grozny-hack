import React from "react";
import Link from "next/link";
import Image from "next/image";

const Sidebar = ({active, children}) => {
    return (
        <div className="flex">
            <div className="fixed w-14 sm:w-20 h-screen p-4 bg-white border-r-[1px] flex flex-col justify-between">
                <div className="flex flex-col items-center">
                    <Link href="/">
                        <div className={active === "first" ? 
                            "rounded-lg bg-blue-500 text-white border p-1" : 
                            "rounded-lg text-blue-500 hover:text-white hover:bg-blue-500 border border-blue-500 p-1"}>
                                <svg fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-9">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 6a7.5 7.5 0 1 0 7.5 7.5h-7.5V6Z" />
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0 0 13.5 3v7.5Z" />
                                </svg>

                            {/* <Image src="/graph.svg" width="40" height="40"></Image> */}
                        </div>
                    </Link>
                    
                    <span className="border-b-[2px] border-gray-200 w-full p-2"></span>
                    
                    <Link href="/upload">
                        <div className={active === "second" ? 
                            "my-4 rounded-lg bg-blue-500 text-white border p-1" : 
                            "my-4 rounded-lg text-blue-500 hover:text-white hover:bg-blue-500 border border-blue-500 p-1"}>
                            {/* <Image src="/data.svg" width="40" height="40"></Image> */}
                            <svg fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-9">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 16.875h3.375m0 0h3.375m-3.375 0V13.5m0 3.375v3.375M6 10.5h2.25a2.25 2.25 0 0 0 2.25-2.25V6a2.25 2.25 0 0 0-2.25-2.25H6A2.25 2.25 0 0 0 3.75 6v2.25A2.25 2.25 0 0 0 6 10.5Zm0 9.75h2.25A2.25 2.25 0 0 0 10.5 18v-2.25a2.25 2.25 0 0 0-2.25-2.25H6a2.25 2.25 0 0 0-2.25 2.25V18A2.25 2.25 0 0 0 6 20.25Zm9.75-9.75H18a2.25 2.25 0 0 0 2.25-2.25V6A2.25 2.25 0 0 0 18 3.75h-2.25A2.25 2.25 0 0 0 13.5 6v2.25a2.25 2.25 0 0 0 2.25 2.25Z" />
                            </svg>

                        </div>
                    </Link>

                    <Link href="/info">
                        <div className={active === "third" ? 
                            "my-4 rounded-lg bg-blue-500 text-white border p-1" : 
                            "my-4 rounded-lg text-blue-500 hover:text-white hover:bg-blue-500 border border-blue-500 p-1"}>
                            <svg fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-9">
                                <path strokeLinecap="round" strokeLinejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                            </svg>
                        </div>
                    </Link>

                    
                    
                    {/* <Link href="/">
                        <div className="border-2 rounded-lg bg-slate-900 border-black ">
                        <svg fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-11 text-white">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 16.875h3.375m0 0h3.375m-3.375 0V13.5m0 3.375v3.375M6 10.5h2.25a2.25 2.25 0 0 0 2.25-2.25V6a2.25 2.25 0 0 0-2.25-2.25H6A2.25 2.25 0 0 0 3.75 6v2.25A2.25 2.25 0 0 0 6 10.5Zm0 9.75h2.25A2.25 2.25 0 0 0 10.5 18v-2.25a2.25 2.25 0 0 0-2.25-2.25H6a2.25 2.25 0 0 0-2.25 2.25V18A2.25 2.25 0 0 0 6 20.25Zm9.75-9.75H18a2.25 2.25 0 0 0 2.25-2.25V6A2.25 2.25 0 0 0 18 3.75h-2.25A2.25 2.25 0 0 0 13.5 6v2.25a2.25 2.25 0 0 0 2.25 2.25Z" />
                        </svg>
                        </div>
                    </Link> */}
                </div>
            </div>
            <main className="ml-14 sm:ml-20 w-full">{children}</main>
        </div>
    )
}




export default Sidebar;