class Attachment {
    constructor(content_type, content_data) {
        this.content_type = content_type;
        this.content_data = content_data;
    }

     static parseObject(data){
        let attm = new Attachment();
        Object.keys(data).forEach((key) => {
            attm[key] = data[key];
        });
        return attm;
    }
}

export default Attachment;