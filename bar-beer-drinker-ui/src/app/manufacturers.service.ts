import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ManufacturersService {

  constructor(private http: HttpClient) {}

  get_manufacturers(){
    return this.http.get<any[]>('/api/manufacturer')
  }



  

}
