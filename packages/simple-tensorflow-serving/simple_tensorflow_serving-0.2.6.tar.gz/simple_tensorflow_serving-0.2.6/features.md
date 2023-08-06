



2. support image:


"image/jpeg"

        elif input_type == 'image/jpeg':
            try:
                for name in input_names:
                    logger.info('Request input: ' + name +  ' should be image with jpeg format.')
                    input_file = self.handler.get_file_data(name)
                    if input_file:
                        mime_type = input_file.content_type
                        assert mime_type == input_type, 'Input data for request argument: %s is not correct. ' \
                                                        '%s is expected but %s is given.' % (name, input_type, mime_type)
                        file_data = input_file.read()
                        assert isinstance(file_data, (str, bytes)), 'Image file buffer should be type str or ' \
                                                                    'bytes, but got %s' % (type(file_data))
                    else:
                        file_data = base64.decodestring(self.handler.get_form_data(name))
                    input_data.append(file_data)
                    
                    
                    
    def get_file_data(self, field=None):
        """
        Get file data from request.
        
        Parameters
        ----------
        field : string 
            Get field data from file data.

        Returns
        ----------
        Object: 
            Field data from file data.
        """
        logger.info('Getting file data from request.')
        files = {k: v[0] for k, v in dict(request.files).items()}
        if field is None:
            return files
        if field in files:
            return files[field]
        return None
                            
                            
        
                            
                            
                            

    def inference(self, data):
        '''
        Wrapper function to run preprocess, inference and postprocess functions.

        Parameters
        ----------
        data : list of object
            Raw input from request.

        Returns
        -------
        list of outputs to be sent back to client.
            data to be sent back
        '''
        pre_start_time = time.time()
        data = self._preprocess(data)
        infer_start_time = time.time()

        # Update preprocess latency metric
        pre_time_in_ms = (infer_start_time - pre_start_time) * 1000
        if self.model_name + '_LatencyPreprocess' in MetricsManager.metrics:
            MetricsManager.metrics[self.model_name + '_LatencyPreprocess'].update(pre_time_in_ms)

        data = self._inference(data)
        data = self._postprocess(data)

        # Update inference latency metric
        infer_time_in_ms = (time.time() - infer_start_time) * 1000
        if self.model_name + '_LatencyInference' in MetricsManager.metrics:
            MetricsManager.metrics[self.model_name + '_LatencyInference'].update(infer_time_in_ms)

        # Update overall latency metric
        if self.model_name + '_LatencyOverall' in MetricsManager.metrics:
            MetricsManager.metrics[self.model_name + '_LatencyOverall'].update(pre_time_in_ms + infer_time_in_ms)

        return data                            
  
                            
                            
                            
                            
                            
                            
    def _preprocess(self, data):
        img_list = []
        for idx, img in enumerate(data):
            input_shape = self.signature['inputs'][idx]['data_shape']
            # We are assuming input shape is NCHW
            [h, w] = input_shape[2:]
            img_arr = image.read(img)
            img_arr = image.resize(img_arr, w, h)
            img_arr = image.transform_shape(img_arr)
            img_list.append(img_arr)
        return img_list

    def _postprocess(self, data):
        assert hasattr(self, 'labels'), \
            "Can't find labels attribute. Did you put synset.txt file into " \
            "model archive or manually load class label file in __init__?"
        return [ndarray.top_probability(d, self.labels, top=5) for d in data]
                                    
                                    
                                    
                                    
                                    
        def _inference(self, data):
            '''Internal inference methods for MXNet. Run forward computation and
            return output.
    
            Parameters
            ----------
            data : list of NDArray
                Preprocessed inputs in NDArray format.
    
            Returns
            -------
            list of NDArray
                Inference output.
            '''
            # Check input shape
            check_input_shape(data, self.signature)
            data = [item.as_in_context(self.ctx) for item in data]
            self.mx_model.forward(DataBatch(data))
            return self.mx_model.get_outputs()                                
                            


 
 
4. tensorflow_tempalte_application support mocking training dataset in memory

6. support basic auth