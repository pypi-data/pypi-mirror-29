All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Description-Content-Type: UNKNOWN
Description: pyred
        =====
        
        A python package to easily send data to Amazon Redshift
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        1) Installation
        '''''''''''''''
        
        Open a terminal and install pyred package
                                                           
        ::
        
            pip install pyred
        
        
        2) Use
        ''''''
        
        1) Be sure that you have set environment variables with Redshift credentials like this:
                                                                                            
        
        ::
        
            export RED_{INSTANCE}_DATABASE=""
            export RED_{INSTANCE}_USERNAME=""
            export RED_{INSTANCE}_HOST=""
            export RED_{INSTANCE}_PORT=""
            export RED_{INSTANCE}_PASSWORD=""
        
        2) Be also sure that your IP address is authorized for the redshift cluster/instance.
                                                                                          
        
        3) Prepare your data like that:
                                    
        
        .. code:: python
        
            data = {
                    "table_name"    : 'name_of_the_redshift_schema' + '.' + 'name_of_the_redshift_table'
                    #Table must already exist
                    "columns_name"  : [first_column_name,second_column_name,...,last_column_name],
                    "rows"      : [[first_raw_value,second_raw_value,...,last_raw_value],...]
                }
        
        4) Send your data (use the same {INSTANCE} parameter as environment variables):
                        
        
        .. code:: python
        
            import pyred
            pyred.send_to_redshift({INSTANCE},data,replace=True)
        
        -  replace (default=True) argument allows you to replace or append data
           in the table
        -  batch\_size (default=1000) argument also exists to send data in
           batchs
        
        3) Example
        ''''''
        You have a table called dog in you animal scheme. This table has two columns : 'name' and 'size'.
        You want to add two dogs (= two rows) : Pif which is big and Milou which is small.
        *data* will be like that:
        
        .. code:: python
        
            data = {
                    "table_name"    : 'animal.dog'
                    "columns_name"  : ['name','size'],
                    "rows"      : [['Pif','big'], ['Milou','small']]
                }
        
Keywords: send data amazon redshift easy
Platform: UNKNOWN
Requires-Python: >=3
