import serial
import serial.tools.list_ports
import time

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    port_list = []
    print("\n--- Available Ports ---")
    for i, port in enumerate(ports):
        print(f"[{i}] {port.device} - {port.description}")
        port_list.append(port.device)
    return port_list

def main():
    try:
        available_ports = list_serial_ports()
        if not available_ports:
            print("ERROR: Walang nahanap na Serial Port!")
            return

        choice = input("\nI-type ang port (e.g. COM3) o index [0]: ")
        
        # Port selection logic
        if choice.isdigit() and int(choice) < len(available_ports):
            selected_port = available_ports[int(choice)]
        else:
            selected_port = choice

        print(f"Kumokonekta sa {selected_port}...")
        
        with serial.Serial(selected_port, 9600, timeout=1) as arduino:
            # Wait a bit for connection to stabilize
            time.sleep(0.5)
            
            while True:
                try:
                    angle = input("\nIlagay angle (0-180): ")
                    if not angle.isdigit() or not (0 <= int(angle) <= 180):
                        print("MALI: Maglagay lamang ng numero mula 0 hanggang 180.")
                        continue
                    
                    # Send command
                    arduino.write(f"{angle}\n".encode())
                    print(f"Command sent: {angle} degrees")
                    
                    # Wait for servo to move
                    time.sleep(1.5) 
                    
                    cont = input("Ituloy? (y/n): ").lower()
                    if cont != 'y': break
                
                except ValueError:
                    print("MALI: Hindi valid na input.")
                except serial.SerialException as e:
                    print(f"SERIAL ERROR: {e}")
                    break

    except serial.SerialException as e:
        print(f"SERIAL ERROR: Hindi mabuksan ang port. Siguraduhing tama ang pinili.\nDetalye: {e}")
    except KeyboardInterrupt:
        print("\nPinatigil ng user ang programa. Paalam!")

if __name__ == "__main__":
    main()