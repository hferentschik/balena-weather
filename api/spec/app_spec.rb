# frozen_string_literal: true

require 'spec_helper'

require_relative '../server'

describe 'App' do
  let(:app) { App.new }

  context 'GET to /' do
    let(:response) { get '/' }

    it 'returns status 200 OK' do
      expect(response.status).to eq 200
    end
  end

  context 'GET to /api/v1/sunrise' do
    let(:response) { get '/api/v1/sunrise' }

    it 'returns status 200 OK' do
      expect(response.status).to eq 200
    end
  end

  context 'GET to /api/v1/sunset' do
    let(:response) { get '/api/v1/sunset' }

    it 'returns status 200 OK' do
      expect(response.status).to eq 200
    end
  end
end
