import { Injectable } from '@angular/core';

import {HttpClient} from '@angular/common/http';

export interface Bar{
  Name: String;
  License: String;
  Address: String;
  City: String;
  State: String;
  Phone: String;
}

export interface BarMenuItem{
  Item: String;
  Manufacturer: String;
  Price: number;
  likes: number; 
}


@Injectable({
  providedIn: 'root'
})
export class BarsService {

  constructor(public http:HttpClient ) { 
    
  }
  getBars(){
    return this.http.get<Bar[]>('/api/bar');

  }
  getBar(bar:String){
    return this.http.get<Bar[]>('/api/bar/'+bar);
  }
  getMenu(bar: String){
    return this.http.get<BarMenuItem[]>('/api/menu/' + bar);
  }
  getFrequentCounts(){
    return this.http.get<any[]>('/api/frequents-data' );
  }

  get_top_drinkers(bar_name: String){
    return this.http.get<any[]>('/api/get_top_drinkers/' + bar_name );
  }

  get_top_beers(bar_name: String){
    return this.http.get<any[]>('/api/get_top_beers/' + bar_name );
  }
}
