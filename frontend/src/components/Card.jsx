const Card = () => {
    return (
        <div className="lg:col-span-2 col-span-1 bg-white flex justify-between w-full border p-4 rounded-lg">
            <div className="flex flex-col w-full pb-4">
                <p className="text-black text-2xl font-bold">Name:</p>
                <p className="text-gray-600">174</p>
            </div>
        </div>
    )
}

export default Card;