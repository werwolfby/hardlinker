import { Injectable } from '@angular/core';
import { Http }       from '@angular/http';
import { Observable } from "rxjs"
import "rxjs/add/operator/map";

export interface FileInfo {
    folder: string;
    path: string[];
    name: string;
}

export interface LinkInfo extends FileInfo {
    links: FileInfo[];
}

const LINKS_API_PATH = 'api/links';

@Injectable()
export class BrowseService {
    constructor (private _http: Http) {        
    }

    getAll() : Observable<LinkInfo[]> {
        return this._http
            .get(LINKS_API_PATH)
            .map(r => <LinkInfo[]> r.json());
    }
}
