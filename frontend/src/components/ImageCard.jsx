const ImageCard = ({id}) => {
    return(
        // <div className="lg:col-span-1 col-span-1 flex justify-between border rounded-lg">
        //     <img
        //     src="https://tecdn.b-cdn.net/img/new/standard/nature/182.jpg"
        //     alt="" />
        // </div>

        <div className="col-span-1 flex justify-between w-[25hv] rounded-l text-surface shadow-secondary-1">
        <div className="flex flex-col relative overflow-hidden bg-cover bg-no-repeat">
            <img
            className="rounded-lg"
                
            src={`http://localhost:8080/api/v2/images/download?id=${id}`}
            alt="" />
        </div>

        </div>
    )
}


export default ImageCard;