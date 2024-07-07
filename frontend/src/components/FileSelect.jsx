
const FileSelect = ({isSended = false, isImageSelected = false, handleImageChange, selectedImage}) => {
    return (
        <div>
            {!isImageSelected &&
              <input className="block w-full text-sm text-gray-500
              file:me-4 file:py-2 file:px-4
              file:rounded-lg
              file:text-sm file:font-semibold
              hover:file:bg-blue-500 hover:file:text-white
              file:disabled:opacity-50 file:disabled:pointer-events-none
              file:border file:border-blue-500 hover:border-transparent rounded
              file:text-blue-700 file:bg-white" 
              disabled={isSended} id="get_image_input" type="file" name="image" accept="zip,application/octet-stream,application/zip,application/x-zip,application/x-zip-compressed" onChange={handleImageChange} />
            }
            {isImageSelected && (
              <>
                <img className="object-cover" src={URL.createObjectURL(selectedImage)} alt="Thumb"  />
              </>
            )}
          </div>
    )
}

export default FileSelect;