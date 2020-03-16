import Attachment from "./Attachment";

class DatabaseModel {
    // synonyms, relations, tags - array;
    constructor(
        _id,
        name,
        russian_name,
        synonyms,
        description,
        russian_description,
        relations,
        tags,
        text,
        creation_date,
        attachments
    ) {
        this._id = _id;
        this.name = name;
        this.russian_name = russian_name;
        this.synonyms = synonyms;
        this.description = description;
        this.russian_description = russian_description;
        this.relations = relations;
        this.tags = tags;
        this.text = text;
        this.creation_date = creation_date;
        this.attachments = attachments;
    }

    setAttachments(attachments){
        this.attachments = attachments;
    }

    addAttachment(attachment){
        this.attachments.push(attachment);
    }

    static parseObject(data) {
        let dbm = new DatabaseModel();
        dbm.setAttachments([]);
        Object.keys(data).forEach((key) => {
            if (key === 'attachments') {
                if (Number(data[key].length) !== 0) {
                    data[key].forEach(element => dbm.addAttachment(Attachment.parseObject(element)));
                }
            } else {
                dbm[key] = data[key];
            }
        });
        return dbm;
    }
}

export default DatabaseModel;