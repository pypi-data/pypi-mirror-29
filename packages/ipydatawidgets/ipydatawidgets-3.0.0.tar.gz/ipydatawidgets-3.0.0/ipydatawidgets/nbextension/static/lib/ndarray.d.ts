/// <reference types="ndarray" />
import { DataModel } from './base';
import { ISerializers } from 'jupyter-dataserializers';
import ndarray = require('ndarray');
export declare class NDArrayModel extends DataModel {
    defaults(): any;
    getNDArray(key?: string): ndarray | null;
    static serializers: ISerializers;
    static model_name: string;
}
