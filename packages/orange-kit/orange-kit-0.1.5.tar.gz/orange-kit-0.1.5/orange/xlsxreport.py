# Xlsx报表库
# 主要是对xlsxwriter进行进一步封装
# 作者：黄涛
# 创建：2015-12-04

from xlsxwriter.utility import xl_col_to_name
from xlsxwriter import Workbook
from xlsxwriter.worksheet import convert_range_args,Worksheet,\
     convert_cell_args,convert_column_args
from orange import *

# 预定义格式
DefaultFormats=(('currency',{'num_format':'#,##0.00'}),
                ('rate',{'num_format':'0.0000%'}),
                ('title',{'font_name':'黑体','font_size':16,
                          'align':'center'}),
                ('h2',{'font_name':'黑体','font_size':12,
                          'align':'center'}),
                ('mh2',{'font_name':'黑体','font_size':12,
                          'align':'center','valign':'vcenter'}),
                ('percent',{'num_format':'0.00%'}),
                ('date',{'num_format':'yyyy-mm-dd'}),
                ('time',{'num_format':'hh:mm:ss'}),
                ('number',{'num_format':'#,##0'}),
                ('datetime',{'num_format':'yyyy-mm-dd hh:mm:ss'}),
                ('timestamp',{'num_format':'yyyy-mm-dd hh:mm:ss.0'}))

class XlsxReport():
    '''
    导出Excel报表，主要的用法：
    data=(('data11','data12'),
          ('data21','data22'))
    columns=[{'header':'标题1',
              'width':11,},
             {'header':'标题2',
              'width':13,
              'format':'currency'}]
    with XlsxReport('xlsx_name')as rpt:
        rpt.add_table('A1','sheetname',columns=columns,data=data)
    '''
    def __init__(self,*args,**kwargs):
        deprecation("XlsxReport","Book")
        self.book=Workbook(*args,**kwargs)
        self.formats={}
        self.add_formats(DefaultFormats)
        self.sheet=None
        self.sheets={}

    def __enter__(self):
        return self

    def __exit__(self,_type,value,trace):
        self.close()

    def ensure_sheet(self,sheet):
        self.get_sheet(sheet)
        if not sheet in self.sheets:
            self.sheets[sheet]=Sheet(self)
        return self.sheets.get(sheet)

    def get_sheet(self,sheetname):
        '''获取工作表，并设为默认工作表'''
        if isinstance(sheetname,Worksheet):
            return sheetname
        for sheet in self.book.worksheets():
            if sheet.name==sheetname:break
        else:
            sheet=self.book.add_worksheet(sheetname)
        self.sheet=sheet
        return sheet

    def set_row(self,row,height=None,format=None,options={}):
        if format:
            format=self.formats.get(format,format)
        self.sheet.set_row(row,height,format,options)

    @convert_column_args
    def set_column(self,firstcol,lastcol,width=None,
                   format=None,options={}):
        if format:
            format=self.formats.get(format,format)
        self.sheet.set_column(firstcol,lastcol,width,format,options)
    
    @convert_range_args
    def mwrite(self,first_row,first_col,last_row,last_col,\
               value,format=None):
        '''合并写入到默认的工作表中'''
        if format:
            format=self.formats.get(format,format)
        self.sheet.merge_range(first_row,first_col,last_row,last_col,
                               value,format)

    @convert_range_args
    def write_formulas(self,*args,**kwargs):
        pass
    
    @convert_cell_args
    def write_formula(self,row,col,formula,format=None,value=0):
        if format:
            format=self.formats.get(format,format)
        self.sheet.write_formula(row,col,formula,format,value)
        
    @convert_cell_args
    def write(self,row,col,value,format=None):
        '''单一单元格写入'''
        if format:
            format=self.formats.get(format,format)
        self.sheet.write(row,col,value,format)

    @convert_cell_args
    def rwrite(self,row,col,values,format=None):
        '''按行写入'''
        if format:
            format=self.formats.get(format,format)
        self.sheet.write_row(row,col,values,format)
        
    def close(self):
        '''关闭文件'''
        self.book.close()

    def add_formats(self,args):
        '''添加格式'''
        if isinstance(args,dict):
            args=args.items()
        self.formats.update({name:self.book.add_format(format) for \
                    name,format in args})
                      
    @convert_range_args
    def add_table(self,first_row,first_col,last_row,last_col,\
                  sheet=None,**kwargs):
        '''添加图表，如sheet为空，则使用默认的工作表'''
        sheet=self.get_sheet(sheet)if sheet else self.sheet
        columns=kwargs.get('columns')
        if columns:
            new_columns=[]
            for idx,column in enumerate(columns):
                if 'width' in column:
                    sheet.set_column("{0}:{0}".format(
                        xl_col_to_name(idx+first_col)),\
                        column.get('width'))
                format=column.get("format")
                if format and isinstance(format,str):
                    new_column=column.copy()
                    new_column['format']=self.formats.get(format)
                    new_columns.append(new_column)
                else:
                    new_columns.append(column)
            kwargs['columns']=new_columns
            last_col=first_col+len(columns)-1
        if 'data' in kwargs:
            last_row=first_row+len(kwargs['data'])
            if kwargs.get('total_row',False):
                last_row+=1
        sheet.add_table(first_row,first_col,last_row,last_col,kwargs)

Pattern=R/r'([A-Z]{1,2})(\d*)([:_]([A-Z]{1,2})(\d*))?'

class Sheet:
    def __init__(self,rpt):
        self.rpt=rpt
        self.row=1

    def write(self,range,value,format=None):
        if ':' in range and not isinstance(value,(dict,tuple,list)):
            self.rpt.mwrite(range,value,format)
        if not ':' in range:
            if isinstance(value,(list,tuple)):
                self.rpt.rwrite(range,value)
            else:
                if isinstance(value,str) and value.startswith('='):
                    value=value.format(self.row)
                self.rpt.write(range,value,format)

    def __add__(self,val):
        self.row+=val
        return self
    
    def __sub__(self,val):
        self.row-=val
        return self
    
    def __setitem__(self,name,val):
        match=Pattern.fullmatch(name)
        if match:
            r=list(match.groups())
            if not r[1]:
                r[1]=str(self.row)
            rg=''.join(r[:2])
            if r[3]:
                if not r[4]:
                    r[4]=str(self.row)
                rg='%s:%s%s'%(rg,r[3],r[4])
            if not isinstance(val,tuple):
                val=(val,)
            self.write(rg,*val)
        else:
            raise Exception('单元格格式不正确')

    def __setattr__(self,name,val):
        try:
            self[name]=val
        except:
            super().__setattr__(name,val)

    def iter_rows(self,count):
        for i in range(count):
            yield self
            self+1
