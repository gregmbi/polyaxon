// Copyright 2018-2020 Polyaxon, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Code generated by go-swagger; DO NOT EDIT.

package projects_v1

// This file was generated by the swagger tool.
// Editing this file might prove futile when you re-run the swagger generate command

import (
	"fmt"
	"io"

	"github.com/go-openapi/runtime"
	"github.com/go-openapi/strfmt"

	"github.com/polyaxon/polyaxon/sdks/go/http_client/v1/service_model"
)

// UnbookmarkProjectReader is a Reader for the UnbookmarkProject structure.
type UnbookmarkProjectReader struct {
	formats strfmt.Registry
}

// ReadResponse reads a server response into the received o.
func (o *UnbookmarkProjectReader) ReadResponse(response runtime.ClientResponse, consumer runtime.Consumer) (interface{}, error) {
	switch response.Code() {
	case 200:
		result := NewUnbookmarkProjectOK()
		if err := result.readResponse(response, consumer, o.formats); err != nil {
			return nil, err
		}
		return result, nil
	case 204:
		result := NewUnbookmarkProjectNoContent()
		if err := result.readResponse(response, consumer, o.formats); err != nil {
			return nil, err
		}
		return result, nil
	case 403:
		result := NewUnbookmarkProjectForbidden()
		if err := result.readResponse(response, consumer, o.formats); err != nil {
			return nil, err
		}
		return nil, result
	case 404:
		result := NewUnbookmarkProjectNotFound()
		if err := result.readResponse(response, consumer, o.formats); err != nil {
			return nil, err
		}
		return nil, result
	default:
		result := NewUnbookmarkProjectDefault(response.Code())
		if err := result.readResponse(response, consumer, o.formats); err != nil {
			return nil, err
		}
		if response.Code()/100 == 2 {
			return result, nil
		}
		return nil, result
	}
}

// NewUnbookmarkProjectOK creates a UnbookmarkProjectOK with default headers values
func NewUnbookmarkProjectOK() *UnbookmarkProjectOK {
	return &UnbookmarkProjectOK{}
}

/*UnbookmarkProjectOK handles this case with default header values.

A successful response.
*/
type UnbookmarkProjectOK struct {
	Payload interface{}
}

func (o *UnbookmarkProjectOK) Error() string {
	return fmt.Sprintf("[DELETE /api/v1/{owner}/{project}/unbookmark][%d] unbookmarkProjectOK  %+v", 200, o.Payload)
}

func (o *UnbookmarkProjectOK) GetPayload() interface{} {
	return o.Payload
}

func (o *UnbookmarkProjectOK) readResponse(response runtime.ClientResponse, consumer runtime.Consumer, formats strfmt.Registry) error {

	// response payload
	if err := consumer.Consume(response.Body(), &o.Payload); err != nil && err != io.EOF {
		return err
	}

	return nil
}

// NewUnbookmarkProjectNoContent creates a UnbookmarkProjectNoContent with default headers values
func NewUnbookmarkProjectNoContent() *UnbookmarkProjectNoContent {
	return &UnbookmarkProjectNoContent{}
}

/*UnbookmarkProjectNoContent handles this case with default header values.

No content.
*/
type UnbookmarkProjectNoContent struct {
	Payload interface{}
}

func (o *UnbookmarkProjectNoContent) Error() string {
	return fmt.Sprintf("[DELETE /api/v1/{owner}/{project}/unbookmark][%d] unbookmarkProjectNoContent  %+v", 204, o.Payload)
}

func (o *UnbookmarkProjectNoContent) GetPayload() interface{} {
	return o.Payload
}

func (o *UnbookmarkProjectNoContent) readResponse(response runtime.ClientResponse, consumer runtime.Consumer, formats strfmt.Registry) error {

	// response payload
	if err := consumer.Consume(response.Body(), &o.Payload); err != nil && err != io.EOF {
		return err
	}

	return nil
}

// NewUnbookmarkProjectForbidden creates a UnbookmarkProjectForbidden with default headers values
func NewUnbookmarkProjectForbidden() *UnbookmarkProjectForbidden {
	return &UnbookmarkProjectForbidden{}
}

/*UnbookmarkProjectForbidden handles this case with default header values.

You don't have permission to access the resource.
*/
type UnbookmarkProjectForbidden struct {
	Payload interface{}
}

func (o *UnbookmarkProjectForbidden) Error() string {
	return fmt.Sprintf("[DELETE /api/v1/{owner}/{project}/unbookmark][%d] unbookmarkProjectForbidden  %+v", 403, o.Payload)
}

func (o *UnbookmarkProjectForbidden) GetPayload() interface{} {
	return o.Payload
}

func (o *UnbookmarkProjectForbidden) readResponse(response runtime.ClientResponse, consumer runtime.Consumer, formats strfmt.Registry) error {

	// response payload
	if err := consumer.Consume(response.Body(), &o.Payload); err != nil && err != io.EOF {
		return err
	}

	return nil
}

// NewUnbookmarkProjectNotFound creates a UnbookmarkProjectNotFound with default headers values
func NewUnbookmarkProjectNotFound() *UnbookmarkProjectNotFound {
	return &UnbookmarkProjectNotFound{}
}

/*UnbookmarkProjectNotFound handles this case with default header values.

Resource does not exist.
*/
type UnbookmarkProjectNotFound struct {
	Payload interface{}
}

func (o *UnbookmarkProjectNotFound) Error() string {
	return fmt.Sprintf("[DELETE /api/v1/{owner}/{project}/unbookmark][%d] unbookmarkProjectNotFound  %+v", 404, o.Payload)
}

func (o *UnbookmarkProjectNotFound) GetPayload() interface{} {
	return o.Payload
}

func (o *UnbookmarkProjectNotFound) readResponse(response runtime.ClientResponse, consumer runtime.Consumer, formats strfmt.Registry) error {

	// response payload
	if err := consumer.Consume(response.Body(), &o.Payload); err != nil && err != io.EOF {
		return err
	}

	return nil
}

// NewUnbookmarkProjectDefault creates a UnbookmarkProjectDefault with default headers values
func NewUnbookmarkProjectDefault(code int) *UnbookmarkProjectDefault {
	return &UnbookmarkProjectDefault{
		_statusCode: code,
	}
}

/*UnbookmarkProjectDefault handles this case with default header values.

An unexpected error response
*/
type UnbookmarkProjectDefault struct {
	_statusCode int

	Payload *service_model.RuntimeError
}

// Code gets the status code for the unbookmark project default response
func (o *UnbookmarkProjectDefault) Code() int {
	return o._statusCode
}

func (o *UnbookmarkProjectDefault) Error() string {
	return fmt.Sprintf("[DELETE /api/v1/{owner}/{project}/unbookmark][%d] UnbookmarkProject default  %+v", o._statusCode, o.Payload)
}

func (o *UnbookmarkProjectDefault) GetPayload() *service_model.RuntimeError {
	return o.Payload
}

func (o *UnbookmarkProjectDefault) readResponse(response runtime.ClientResponse, consumer runtime.Consumer, formats strfmt.Registry) error {

	o.Payload = new(service_model.RuntimeError)

	// response payload
	if err := consumer.Consume(response.Body(), o.Payload); err != nil && err != io.EOF {
		return err
	}

	return nil
}
