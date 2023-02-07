from subprocess import check_output,CalledProcessError

# list_all_networks_cmd:list[str]=['netsh', 'wlan','show','profiles']

# list_output:str=check_output(list_all_networks_cmd,shell=True).decode()

# networks_names=[outline.rsplit(":")[-1].strip() for outline in list_output.split("\n")][9:]

#get_key_cmd=["netsh", "wlan", "show", "profile", "name=Eye-Fi Card 22eade", "key=clear", "|", "find", "/I", 'Key Content']


#print(check_output(get_key_cmd,shell="True"))

#for network_name in networks_names:
    


#print("\n".join([f"{i} {network}" for i,network in enumerate(networks_names) if len(network)>2]))



class KnownNetwork:
    def __init__(self,name:str):
        self.name:str=name
        self.key:str|None=self.get_key()
        
        
    def get_key(self)->None|str:
        get_key_cmd=["netsh", "wlan", "show", "profile", "name="+self.name, "key=clear", "|", "find", "/I", 'Key Content']
        try:
            raw:str=check_output(get_key_cmd,shell=True).decode()
            print(".",end="")
        except CalledProcessError as e:
            print("x",end="")
            return None
        return raw.split(":")[-1].strip()
        
    def __str__(self) -> str:
        return f'{self.name} = {self.key}'


class AllNetworks:
    
    def __init__(self):
        list_all_networks_cmd:list[str]=['netsh', 'wlan','show','profiles']
        list_output:str=check_output(list_all_networks_cmd,shell=True).decode()

        possible_network_names=[outline.rsplit(":")[-1].strip() for outline in list_output.split("\n")][9:]
        
        temp_networks:dict={}
        
        for name in possible_network_names:
            net=KnownNetwork(name)
            if net.key is not None:
                temp_networks[name]=net
                
        # Sorted keys
        
        keyset=sorted(temp_networks.keys())
        
        self.networks={key:temp_networks[key] for key in keyset}
                
        print(f"\n\nFound all {len(self.networks)}\n\n")
        
    def __str__(self):
        return "\n".join([str(net) for net in self.networks.values()])
    
    def __repr__(self):
        return str(self)
        
    
    
if __name__=="__main__":
    nets=AllNetworks()
    print(nets)