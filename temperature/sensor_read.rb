# frozen_string_literal: true

require 'ds18b20'
require 'json'
require 'logger'
require 'mqtt'
require 'rufus-scheduler'

logger = Logger.new($stdout)

# Sensor defines a single DS18B20 sensor
class Sensor
  attr_reader :id, :name

  def initialize(name, id = nil)
    @name = name
    id = default_id if id.nil?
    @id = id
  end

  def default_id
    abort 'no /sys/bus/w1/devices directory' unless Dir.exist? '/sys/bus/w1/devices'
    sensors = Dir.entries('/sys/bus/w1/devices').select do |entry|
      File.directory? File.join('/sys/bus/w1/devices', entry) and entry.start_with?('28-')
    end
    abort 'no sensors mounted under /sys/bus/w1/devices' if sensors.empty?
    sensors[0]
  end

  def read_temperature
    Ds18b20::Parser.new("/sys/bus/w1/devices/#{id}/w1_slave").celsius
  end
end

FakeSensor = Struct.new(:name, :id) do
  def read_temperature
    rand(-20..40)
  end
end

broker_address = ENV.fetch('MQTT_BROKER', 'mqtt')
sample_rate = ENV.fetch('SAMPLE_RATE', 60).to_i

if Dir.exist? '/sys/bus/w1/devices'
  sensor = Sensor.new('temperature')
else
  logger.info "using fake sensor"
  sensor = FakeSensor.new 'fake_sensor', 'fake'
end


logger.info "creating scheduler for sensor '#{sensor.id}' with sample rate #{sample_rate} seconds"
scheduler = Rufus::Scheduler.new
scheduler.every sample_rate, first: :now do
  measurement = sensor.read_temperature
  now = Time.new
  payload = {
    :time => now.strftime("%Y-%m-%dT%T"),
    :measurement => 'temperature',
    :fields => {
      :value => measurement,
      :sensor => 'DS18B20'
    }
  }

  json_payload = JSON[payload]
  logger.info "new measurement: #{json_payload}"
  begin
   MQTT::Client.connect(:host => broker_address, :username => ENV['MQTT_USER'], :password => ENV['MQTT_PASSWORD'],) do |c|
    c.publish('sensors', json_payload)
   end
  rescue Exception => e
    logger.info "unable to connect or publish to MQTT client: #{e.message}"
  end
end

scheduler.join
