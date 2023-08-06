/// <reference types="ndarray" />
import { WidgetModel } from '@jupyter-widgets/base';
import { ISerializers, IDataSource } from 'jupyter-dataserializers';
import ndarray = require('ndarray');
export declare abstract class DataModel extends WidgetModel implements IDataSource {
    defaults(): any;
    abstract getNDArray(key?: string): ndarray | null;
    static serializers: ISerializers;
    static model_module: string;
    static model_module_version: string;
    static view_name: null;
    static view_module: null;
    static view_module_version: string;
}
